import base64
import copy
import hashlib
import pytest
import runes
import string
from typing import Sequence


# This is a simplified version of end_shastream
def end_shastream_simple(length: int) -> bytes:
    stream = bytes([0x80])
    while ((length + len(stream) + 8) % 64) != 0:
        stream += bytes(1)
    stream += int.to_bytes(length * 8, 8, 'big')
    return stream


def check_auth_sha(secret: bytes, restrictions: Sequence[runes.Restriction]):
    stream = secret

    for r in restrictions:
        stream += end_shastream_simple(len(stream))
        stream += bytes(r.encode(), encoding='utf8')

    return hashlib.sha256(stream).digest()


def test_end_shastream():
    # Make sure it gives same as our naive approach
    for length in range(0, 100):
        assert runes.end_shastream(length) == end_shastream_simple(length)


def test_rune_auth():
    # Rune with 16x0 secret.
    secret = bytes(16)
    mr = runes.MasterRune(secret)

    assert check_auth_sha(secret, []) == mr.authcode()
    assert mr.is_rune_authorized(runes.Rune.from_authcode(mr.authcode(), []))

    restriction = runes.Restriction([runes.Alternative('f1', '=', 'v1')])
    mr.add_restriction(restriction)

    assert check_auth_sha(secret, [restriction]) == mr.authcode()
    assert not mr.is_rune_authorized(runes.Rune.from_authcode(mr.authcode(), []))
    assert mr.is_rune_authorized(runes.Rune.from_authcode(mr.authcode(), [restriction]))

    long_restriction = runes.Restriction([runes.Alternative('f' * 32, '=', 'v1' * 64)])
    mr.add_restriction(long_restriction)

    assert check_auth_sha(secret, [restriction, long_restriction]) == mr.authcode()
    assert not mr.is_rune_authorized(runes.Rune.from_authcode(mr.authcode(), [restriction]))
    assert not mr.is_rune_authorized(runes.Rune.from_authcode(mr.authcode(), [long_restriction]))
    assert not mr.is_rune_authorized(runes.Rune.from_authcode(mr.authcode(), [long_restriction, restriction]))
    assert mr.is_rune_authorized(runes.Rune.from_authcode(mr.authcode(), [restriction, long_restriction]))


def test_rune_alternatives():
    """Test that we interpret alternatives as expected"""
    alt = runes.Alternative('f1', '!', '')
    assert alt.test({}) is None
    assert alt.test({'f1': '1'}) == 'f1: is present'
    assert alt.test({'f2': '1'}) is None

    alt = runes.Alternative('f1', '=', '1')
    assert alt.test({}) == 'f1: is missing'
    assert alt.test({'f1': '1'}) is None
    assert alt.test({'f1': '01'}) == 'f1: != 1'
    assert alt.test({'f1': '10'}) == 'f1: != 1'
    assert alt.test({'f1': '010'}) == 'f1: != 1'
    assert alt.test({'f1': '10101'}) == 'f1: != 1'

    alt = runes.Alternative('f1', '/', '1')
    assert alt.test({}) == 'f1: is missing'
    assert alt.test({'f1': '1'}) == 'f1: = 1'
    assert alt.test({'f1': '01'}) is None
    assert alt.test({'f1': '10'}) is None
    assert alt.test({'f1': '010'}) is None
    assert alt.test({'f1': '10101'}) is None

    alt = runes.Alternative('f1', '$', '1')
    assert alt.test({}) == 'f1: is missing'
    assert alt.test({'f1': '1'}) is None
    assert alt.test({'f1': '01'}) is None
    assert alt.test({'f1': '10'}) == 'f1: does not end with 1'
    assert alt.test({'f1': '010'}) == 'f1: does not end with 1'
    assert alt.test({'f1': '10101'}) is None

    alt = runes.Alternative('f1', '^', '1')
    assert alt.test({}) == 'f1: is missing'
    assert alt.test({'f1': '1'}) is None
    assert alt.test({'f1': '01'}) == 'f1: does not start with 1'
    assert alt.test({'f1': '10'}) is None
    assert alt.test({'f1': '010'}) == 'f1: does not start with 1'
    assert alt.test({'f1': '10101'}) is None

    alt = runes.Alternative('f1', '~', '1')
    assert alt.test({}) == 'f1: is missing'
    assert alt.test({'f1': '1'}) is None
    assert alt.test({'f1': '01'}) is None
    assert alt.test({'f1': '10'}) is None
    assert alt.test({'f1': '010'}) is None
    assert alt.test({'f1': '10101'}) is None
    assert alt.test({'f1': '020'}) == 'f1: does not contain 1'

    alt = runes.Alternative('f1', '<', '1')
    assert alt.test({}) == 'f1: is missing'
    assert alt.test({'f1': '1'}) == 'f1: >= 1'
    assert alt.test({'f1': '01'}) == 'f1: >= 1'
    assert alt.test({'f1': '10'}) == 'f1: >= 1'
    assert alt.test({'f1': '010'}) == 'f1: >= 1'
    assert alt.test({'f1': '10101'}) == 'f1: >= 1'
    assert alt.test({'f1': '020'}) == 'f1: >= 1'
    assert alt.test({'f1': '0'}) is None
    assert alt.test({'f1': 'x'}) == 'f1: not an integer field'

    alt = runes.Alternative('f1', '<', 'x')
    assert alt.test({}) == 'f1: is missing'
    assert alt.test({'f1': '1'}) == 'f1: not a valid integer'

    alt = runes.Alternative('f1', '>', '1')
    assert alt.test({}) == 'f1: is missing'
    assert alt.test({'f1': '1'}) == 'f1: <= 1'
    assert alt.test({'f1': '01'}) == 'f1: <= 1'
    assert alt.test({'f1': '10'}) is None
    assert alt.test({'f1': '010'}) is None
    assert alt.test({'f1': '10101'}) is None
    assert alt.test({'f1': '020'}) is None
    assert alt.test({'f1': '0'}) == 'f1: <= 1'
    assert alt.test({'f1': 'x'}) == 'f1: not an integer field'

    alt = runes.Alternative('f1', '>', 'x')
    assert alt.test({}) == 'f1: is missing'
    assert alt.test({'f1': '1'}) == 'f1: not a valid integer'

    alt = runes.Alternative('f1', '{', '1')
    assert alt.test({}) == 'f1: is missing'
    assert alt.test({'f1': '1'}) == 'f1: is the same or ordered after 1'
    assert alt.test({'f1': '01'}) is None
    assert alt.test({'f1': '10'}) == 'f1: is the same or ordered after 1'
    assert alt.test({'f1': '010'}) is None
    assert alt.test({'f1': '10101'}) == 'f1: is the same or ordered after 1'
    assert alt.test({'f1': '020'}) is None
    assert alt.test({'f1': '0'}) is None

    alt = runes.Alternative('f1', '}', '1')
    assert alt.test({}) == 'f1: is missing'
    assert alt.test({'f1': '1'}) == 'f1: is the same or ordered before 1'
    assert alt.test({'f1': '01'}) == 'f1: is the same or ordered before 1'
    assert alt.test({'f1': '10'}) is None
    assert alt.test({'f1': '010'}) == 'f1: is the same or ordered before 1'
    assert alt.test({'f1': '10101'}) is None
    assert alt.test({'f1': '020'}) == 'f1: is the same or ordered before 1'
    assert alt.test({'f1': '0'}) == 'f1: is the same or ordered before 1'

    alt = runes.Alternative('f1', '#', '1')
    assert alt.test({}) is None
    assert alt.test({'f1': '1'}) is None
    assert alt.test({'f1': '01'}) is None
    assert alt.test({'f1': '10'}) is None
    assert alt.test({'f1': '010'}) is None
    assert alt.test({'f1': '10101'}) is None
    assert alt.test({'f1': '020'}) is None
    assert alt.test({'f1': '0'}) is None


def test_rune_restriction():
    alt1 = runes.Alternative('f1', '!', '')
    alt2 = runes.Alternative('f2', '=', '2')

    # Either can be true
    restr = runes.Restriction((alt1, alt2))
    assert restr.test({}) is None
    assert restr.test({'f1': '1', 'f2': 3}) == "f1: is present AND f2: != 2"
    assert restr.test({'f2': '1'}) is None
    assert restr.test({'f2': '2'}) is None
    assert restr.test({'f2': 2}) is None


def test_rune_restrictions():
    """Either of these passes, the restriction passes"""
    alt1 = runes.Alternative('f1', '!', '')
    alt2 = runes.Alternative('f2', '=', '2')

    rune = runes.Rune(bytes(32), restrictions=[runes.Restriction((alt1, alt2))])
    assert rune.are_restrictions_met({}) == (True, '')
    assert (rune.are_restrictions_met({'f1': '1', 'f2': 3})
            == (False, 'f1: is present AND f2: != 2'))
    assert rune.are_restrictions_met({'f1': '1', 'f2': 2}) == (True, '')
    assert rune.are_restrictions_met({'f2': '1'}) == (True, '')
    assert rune.are_restrictions_met({'f2': '2'}) == (True, '')

    alt3 = runes.Alternative('f3', '>', '2')
    rune = runes.Rune(bytes(32), restrictions=[runes.Restriction((alt1, alt2)),
                                               runes.Restriction((alt3,))])
    assert rune.are_restrictions_met({}) == (False, 'f3: is missing')
    assert (rune.are_restrictions_met({'f1': '1', 'f2': 3})
            == (False, 'f1: is present AND f2: != 2'))
    assert (rune.are_restrictions_met({'f1': '1', 'f2': 2})
            == (False, 'f3: is missing'))
    assert rune.are_restrictions_met({'f2': '1'}) == (False, 'f3: is missing')
    assert rune.are_restrictions_met({'f2': '2'}) == (False, 'f3: is missing')
    assert rune.are_restrictions_met({'f3': '2'}) == (False, 'f3: <= 2')
    assert rune.are_restrictions_met({'f3': '3'}) == (True, '')
    assert (rune.are_restrictions_met({'f1': '1', 'f2': 'x', 'f3': 3})
            == (False, 'f1: is present AND f2: != 2'))
    assert (rune.are_restrictions_met({'f2': '1', 'f3': 2})
            == (False, 'f3: <= 2'))
    assert (rune.are_restrictions_met({'f2': '2', 'f3': 2})
            == (False, 'f3: <= 2'))
    assert rune.are_restrictions_met({'f2': '1', 'f3': 3}) == (True, '')
    assert rune.are_restrictions_met({'f2': '2', 'f3': 4}) == (True, '')


def test_rune_fromstring_norestrictions():
    rune = runes.Rune.from_base64('-YpZTBZ4Tb5SsUz3XIukxBx'
                                  'R619iEthm9oNJnC0LxZM=')
    assert rune.restrictions == []


def test_copy():
    """Make sure copies get their own sha state, as it corresponds to the restrictions list, which *is* copied"""
    mr = runes.MasterRune(bytes(16))
    mrstring = mr.to_base64()

    # .copy() and copy module should work the same.
    for mrune in (mr.copy(), copy.copy(mr), copy.deepcopy(mr)):
        restriction = runes.Restriction([runes.Alternative('f1', '=', 'v1')])
        mrune.add_restriction(restriction)
        assert mrune.to_base64() != mrstring
        assert mr.to_base64() == mrstring

    # Should work on normal runes, as well.
    orig = runes.Rune.from_base64(mr.to_base64())
    for rune in (orig.copy(), copy.copy(orig), copy.deepcopy(orig)):
        restriction = runes.Restriction([runes.Alternative('f1', '=', 'v1')])
        rune.add_restriction(restriction)
        assert rune.to_base64() != mrstring
        assert orig.to_base64() == mrstring


def test_rune_tostring():
    alt1 = runes.Alternative('f1', '!', '')
    alt2 = runes.Alternative('f2', '=', '2')
    alt3 = runes.Alternative('f3', '>', '2')

    # Either can be true
    restr1 = runes.Restriction((alt1, alt2))
    restr2 = runes.Restriction((alt3,))

    rune = runes.MasterRune(bytes([1] * 32), [restr1, restr2])
    runestr = rune.to_base64()
    rune2 = runes.Rune.from_base64(runestr)

    assert rune == rune2


def test_check():
    # Rune with 16x0 secret.
    secret = bytes(16)
    mr = runes.MasterRune(secret)
    rune = runes.Rune(mr.authcode(),
                      restrictions=[runes.Restriction.from_str('foo=bar')])
    runestr = rune.to_base64()

    # MasterRune variants work
    assert mr.check_with_reason(runestr, {'foo': 'bar'}) == (True, '')
    assert mr.check_with_reason(runestr, {'foo': 'baz'}) == (False, 'foo: != bar')

    assert runes.check_with_reason(secret, runestr, {'foo': 'bar'}) == (True, '')
    assert (runes.check_with_reason(secret, runestr, {'foo': 'baz'})
            == (False, 'foo: != bar'))

    assert runes.check(secret, runestr, {'foo': 'bar'})
    assert not runes.check(secret, runestr, {'foo': 'baz'})


def test_field_with_punctuation():
    rune = runes.Rune(bytes(32), restrictions=[runes.Restriction.from_str('foo=bar.baz')])
    runestr = rune.to_base64()

    rune2 = runes.Rune.from_base64(runestr)
    assert rune == rune2

    # You can add any punctuation this way...
    alt = runes.Alternative.from_str("foo=" + string.punctuation)
    alt2, remainder = runes.Alternative.decode(alt.encode())
    assert remainder == ''
    assert alt == alt2

    restr = runes.Restriction([alt])
    assert restr.encode() == "foo=" + string.punctuation.replace('\\', '\\\\').replace('&', '\\&').replace('|', '\\|')
    restr2, remainder = runes.Restriction.decode(restr.encode())
    assert remainder == ''
    assert restr == restr2
    rune.add_restriction(restr)

    # | and & get escaped on demarshal.
    decoded = base64.urlsafe_b64decode(rune.to_base64())[32:].decode('utf8')
    assert decoded == 'foo=bar.baz' + '&' + 'foo=' + string.punctuation.replace('\\', '\\\\').replace('&', '\\&').replace('|', '\\|')

    rune.add_restriction(runes.Restriction.from_str("foo=1"))
    decoded = base64.urlsafe_b64decode(rune.to_base64())[32:].decode('utf8')
    assert decoded == 'foo=bar.baz' + '&' + 'foo=' + string.punctuation.replace('\\', '\\\\').replace('&', '\\&').replace('|', '\\|') + '&' + 'foo=1'

    runestr = rune.to_base64()
    rune2 = runes.Rune.from_base64(runestr)
    assert rune == rune2


def test_value_callable():
    def callme_pass(alt: runes.Alternative):
        return None

    def callme_fail(alt: runes.Alternative):
        return "failed"

    restr = runes.Restriction.from_str('callme=bar.baz')
    assert restr.test({'callme': callme_pass}) == None
    assert restr.test({'callme': callme_fail}) == "failed"


def test_id():
    secret = bytes(16)
    mr = runes.MasterRune(secret, unique_id=1)

    assert len(mr.restrictions) == 1
    assert mr.restrictions[0].encode() == '=1'

    # id tag is ignored automatically by default.
    assert mr.are_restrictions_met({}) == (True, '')

    # But we can insist on it (usually we'd use a call though)
    assert mr.are_restrictions_met({'': '1'}) == (True, '')
    assert mr.are_restrictions_met({'': '2'}) == (False, ': != 1')

    # id tags with non-empty versions are failed by default!
    mr = runes.MasterRune(secret, unique_id=1, version='2')

    assert len(mr.restrictions) == 1
    assert mr.restrictions[0].encode() == '=1-2'

    assert mr.are_restrictions_met({}) == (False, 'id: unknown version 1-2')

    # But we can insist on it (usually we'd use a call though)
    assert mr.are_restrictions_met({'': '1'}) == (False, ': != 1-2')
    assert mr.are_restrictions_met({'': '1-2'}) == (True, '')


def test_unique_id_restrictions():
    secret = bytes(16)
    mr = runes.MasterRune(secret, unique_id=1)

    alt1 = runes.Alternative('', '=', '2', allow_idfield=True)

    # Don't let them override unique id
    rune = mr.copy()
    rune.add_restriction(alt1)
    with pytest.raises(ValueError, match="unique_id field not valid here"):
        runes.Rune.from_base64(rune.to_base64())

    # Simple sanity checks on unique id if provided.
    rune = copy.deepcopy(mr)
    for cond in ('!', '/', '^', '$', '~', '<', '>', '}', '{', '#'):
        rune.restrictions[0].alternatives[0].cond = cond
        with pytest.raises(ValueError, match="unique_id condition must be '='"):
            runes.Rune.from_base64(rune.to_base64())

    # Can't have multiple alternatives in uniqueid
    secret = bytes(16)
    mr = runes.MasterRune(secret)
    alt2 = runes.Alternative('f', '=', '1')
    mr.add_restriction(runes.Restriction([alt1, alt2]))
    with pytest.raises(ValueError, match="unique_id field cannot have alternatives"):
        runes.Rune.from_base64(mr.to_base64())

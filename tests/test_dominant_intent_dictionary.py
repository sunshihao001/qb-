from modules.wallet_structure.chinese_judgement import zh


def test_professional_dominant_intent_codes_translate_to_chinese():
    assert zh('motive', 'ACCUMULATE') == '疑似吸筹'
    assert zh('motive', 'CONTROL') == '疑似控盘'
    assert zh('motive', 'WASHOUT') == '疑似洗盘'
    assert zh('motive', 'BREAKOUT_TEST') == '疑似测试突破'
    assert zh('motive', 'MARKUP') == '疑似推进拉升'
    assert zh('motive', 'PARTIAL_DISTRIBUTION') == '疑似部分派发'
    assert zh('motive', 'ACTIVE_DISTRIBUTION') == '疑似主动派发'
    assert zh('motive', 'REACCUMULATION') == '疑似再吸筹'
    assert zh('motive', 'REACTIVATION') == '疑似再激活'
    assert zh('motive', 'ABANDONMENT') == '疑似放弃维护'


def test_legacy_motive_codes_remain_supported():
    assert zh('motive', 'POSSIBLE_ACCUMULATION') == '疑似吸筹'
    assert zh('motive', 'POSSIBLE_CONTROL') == '疑似控盘'
    assert zh('motive', 'POSSIBLE_WASHING') == '疑似洗盘'
    assert zh('motive', 'POSSIBLE_PUSH_UP') == '疑似推进拉升'
    assert zh('motive', 'POSSIBLE_ABANDON_CONTROL') == '疑似放弃维护'

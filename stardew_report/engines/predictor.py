# Python port of the pinned upstream calculation rules.
# Rules: MouseyPounds, MIT. Source locations accompany every function.
from ..runtime import *
from ..data import load_table

def table(index):
    return wrap(load_table('predictor', index))
def addCommas_1(parent, this, args):
    # Upstream predictor: 42
    e = Env(parent)
    e.declare([])
    e.local['arguments'] = Array(args)
    e.local['x'] = (args[0] if len(args) > 0 and args[0] is not U else U)
    return call(get(call(get(e['x'], 'toString')), 'replace'), Regex('\\B(?=(?:\\d{3})+(?!\\d))', 'g'), ',')
    return U


def capitalize_2(parent, this, args):
    # Upstream predictor: 47
    e = Env(parent)
    e.declare([])
    e.local['arguments'] = Array(args)
    e.local['s'] = (args[0] if len(args) > 0 and args[0] is not U else U)
    return (binary('+', call(get(get(e['s'], 0), 'toUpperCase')), call(get(e['s'], 'slice'), 1)) if truth(_logic3 := e['s']) else _logic3)
    return U


def compareSemVer_4(parent, this, args):
    # Upstream predictor: 52
    e = Env(parent)
    e.declare(['i', 'na', 'nb', 'pa', 'pb'])
    e.local['arguments'] = Array(args)
    e.local['a'] = (args[0] if len(args) > 0 and args[0] is not U else U)
    e.local['b'] = (args[1] if len(args) > 1 and args[1] is not U else U)
    e.set('pa', call(get(e['a'], 'split'), '.'))
    e.set('pb', call(get(e['b'], 'split'), '.'))
    e.set('i', 0)
    while truth(binary('<', e['i'], 3)):
        e.set('na', call(e['Number'], get(e['pa'], e['i'])))
        e.set('nb', call(e['Number'], get(e['pb'], e['i'])))
        if truth(binary('>', e['na'], e['nb'])):
            return 1
        if truth(binary('>', e['nb'], e['na'])):
            return unary('-', 1)
        if truth((call(e['isNaN'], e['nb']) if truth(_logic5 := unary('!', call(e['isNaN'], e['na']))) else _logic5)):
            return 1
        if truth((unary('!', call(e['isNaN'], e['nb'])) if truth(_logic6 := call(e['isNaN'], e['na'])) else _logic6)):
            return unary('-', 1)
        update_env(e, 'i', 1, False)
    return 0
    return U


def wikify_7(parent, this, args):
    # Upstream predictor: 67
    e = Env(parent)
    e.declare(['trimmed'])
    e.local['arguments'] = Array(args)
    e.local['item'] = (args[0] if len(args) > 0 and args[0] is not U else U)
    e.local['page'] = (args[1] if len(args) > 1 and args[1] is not U else U)
    if truth(binary('==', unary('typeof', e['item']), 'undefined')):
        return 'undefined'
    e.set('trimmed', call(get(e['item'], 'replace'), ' (White)', ''))
    e.set('trimmed', call(get(e['trimmed'], 'replace'), ' (Brown)', ''))
    e.set('trimmed', call(get(e['trimmed'], 'replace'), ' (Any)', ''))
    e.set('trimmed', call(get(e['trimmed'], 'replace'), Regex(' \\(\\d+\\)', ''), ''))
    e.set('trimmed', call(get(e['trimmed'], 'replace'), Regex(' ', 'g'), '_'))
    return (binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', '<a href="https://stardewvalleywiki.com/', e['page']), '#'), e['trimmed']), '">'), e['item']), '</a>') if truth(e['page']) else binary('+', binary('+', binary('+', binary('+', '<a href="https://stardewvalleywiki.com/', e['trimmed']), '">'), e['item']), '</a>'))
    return U


def callback_9(parent, this, args):
    # Upstream predictor: 3480
    e = Env(parent)
    e.declare(['key', 'value'])
    e.local['arguments'] = Array(args)
    e.set('key', call(get(call(get(call(e['$'], this), 'find'), 'key > string'), 'text')))
    e.set('value', call(get(call(get(call(e['$'], this), 'find'), 'value > *'), 'text')))
    if truth(binary('===', e['key'], 'geodesCracked')):
        e.set('geodesCracked', call(e['Number'], e['value']))
    else:
        if truth(binary('===', e['key'], 'daysPlayed')):
            put(e['save'], 'daysPlayed', call(e['Number'], e['value']))
        else:
            if truth(binary('===', e['key'], 'MysteryBoxesOpened')):
                e.set('mysteryBoxesOpened', call(e['Number'], e['value']))
            else:
                if truth(binary('===', e['key'], 'ticketPrizesClaimed')):
                    e.set('ticketPrizesClaimed', call(e['Number'], e['value']))
                else:
                    if truth(binary('===', e['key'], 'timesEnchanted')):
                        e.set('timesEnchanted', call(e['Number'], e['value']))
                    else:
                        if truth(binary('===', e['key'], 'trashCansChecked')):
                            e.set('trashCansChecked', call(e['Number'], e['value']))
                        else:
                            if truth(binary('===', e['key'], 'Book_Trash')):
                                if truth(binary('>', call(e['Number'], e['value']), 0)):
                                    put(e['save'], 'hasGarbageBook', True)
    return U


def callback_12(parent, this, args):
    # Upstream predictor: 3516
    e = Env(parent)
    e.declare(['key', 'value'])
    e.local['arguments'] = Array(args)
    e.set('key', call(get(call(get(call(e['$'], this), 'find'), 'key > string'), 'text')))
    e.set('value', call(get(call(get(call(e['$'], this), 'find'), 'value > *'), 'text')))
    if truth(binary('===', e['key'], 'geodesCracked')):
        e.set('geodesCracked', call(e['Number'], e['value']))
    else:
        if truth(binary('===', e['key'], 'MysteryBoxesOpened')):
            e.set('mysteryBoxesOpened', call(e['Number'], e['value']))
        else:
            if truth(binary('===', e['key'], 'ticketPrizesClaimed')):
                e.set('ticketPrizesClaimed', call(e['Number'], e['value']))
            else:
                if truth(binary('===', e['key'], 'timesEnchanted')):
                    e.set('timesEnchanted', call(e['Number'], e['value']))
                else:
                    if truth(binary('===', e['key'], 'trashCansChecked')):
                        e.set('trashCansChecked', call(e['Number'], e['value']))
    return U


def callback_10(parent, this, args):
    # Upstream predictor: 3506
    e = Env(parent)
    e.declare(['name', 'user'])
    e.local['arguments'] = Array(args)
    e.set('name', call(get(call(get(call(e['$'], this), 'find'), 'name'), 'html')))
    e.set('user', call(get(call(get(call(e['$'], this), 'find'), 'userID'), 'text')))
    e.set('geodesCracked', 0)
    e.set('mysteryBoxesOpened', 0)
    e.set('timesEnchanted', 0)
    if truth((_logic11 if truth(_logic11 := binary('!==', e['name'], '')) else binary('!==', e['user'], ''))):
        call(get(get(e['save'], 'names'), 'push'), e['name'])
        call(get(get(e['save'], 'gender'), 'push'), call(get(call(get(call(get(call(e['$'], this), 'children'), 'gender'), 'first')), 'text')))
        call(get(get(e['save'], 'mp_ids'), 'push'), call(e['bigInt'], call(get(call(get(call(e['$'], this), 'find'), 'UniqueMultiplayerID'), 'text'))))
        call(get(call(get(call(e['$'], this), 'find'), 'stats > Values > item'), 'each'), Fn(callback_12, e))
        call(get(get(e['save'], 'geodesCracked'), 'push'), e['geodesCracked'])
        call(get(get(e['save'], 'mysteryBoxesOpened'), 'push'), e['mysteryBoxesOpened'])
        call(get(get(e['save'], 'ticketPrizesClaimed'), 'push'), e['ticketPrizesClaimed'])
        call(get(get(e['save'], 'timesEnchanted'), 'push'), e['timesEnchanted'])
        call(get(get(e['save'], 'trashCansChecked'), 'push'), e['trashCansChecked'])
    return U


def callback_13(parent, this, args):
    # Upstream predictor: 3545
    e = Env(parent)
    e.declare([])
    e.local['arguments'] = Array(args)
    call(get(get(e['save'], 'names'), 'push'), call(get(call(get(call(e['$'], this), 'find'), 'name'), 'html')))
    call(get(get(e['save'], 'gender'), 'push'), ('Male' if truth(binary('==', call(get(call(get(call(get(call(e['$'], this), 'find'), 'isMale'), 'first')), 'text')), 'true')) else 'Female'))
    call(get(get(e['save'], 'mp_ids'), 'push'), call(e['bigInt'], call(get(call(get(call(e['$'], this), 'find'), 'UniqueMultiplayerID'), 'text'))))
    call(get(get(e['save'], 'geodesCracked'), 'push'), call(e['Number'], call(get(call(get(call(e['$'], this), 'find'), 'stats > geodesCracked'), 'text'))))
    return U


def callback_14(parent, this, args):
    # Upstream predictor: 3558
    e = Env(parent)
    e.declare(['key'])
    e.local['arguments'] = Array(args)
    e.set('key', call(get(call(get(call(e['$'], this), 'find'), 'key > string'), 'text')))
    if truth(binary('===', e['key'], 'timesEnchanted')):
        e.set('timesEnchanted', call(e['Number'], call(get(call(get(call(e['$'], this), 'find'), 'value > unsignedInt'), 'text'))))
    else:
        if truth(binary('===', e['key'], 'trashCansChecked')):
            e.set('trashCansChecked', call(e['Number'], call(get(call(get(call(e['$'], this), 'find'), 'value > unsignedInt'), 'text'))))
    return U


def callback_16(parent, this, args):
    # Upstream predictor: 3571
    e = Env(parent)
    e.declare(['key'])
    e.local['arguments'] = Array(args)
    e.set('key', call(get(call(get(call(e['$'], this), 'find'), 'key > string'), 'text')))
    if truth(binary('===', e['key'], 'timesEnchanted')):
        e.set('timesEnchanted', call(e['Number'], call(get(call(get(call(e['$'], this), 'find'), 'value > unsignedInt'), 'text'))))
    else:
        if truth(binary('===', e['key'], 'trashCansChecked')):
            e.set('trashCansChecked', call(e['Number'], call(get(call(get(call(e['$'], this), 'find'), 'value > unsignedInt'), 'text'))))
    return U


def callback_15(parent, this, args):
    # Upstream predictor: 3568
    e = Env(parent)
    e.declare([])
    e.local['arguments'] = Array(args)
    e.set('timesEnchanted', 0)
    e.set('trashCansChecked', 0)
    call(get(call(get(call(e['$'], this), 'find'), 'stats > stat_dictionary > item'), 'each'), Fn(callback_16, e))
    call(get(get(e['save'], 'timesEnchanted'), 'push'), e['timesEnchanted'])
    call(get(get(e['save'], 'trashCansChecked'), 'push'), e['trashCansChecked'])
    return U


def callback_18(parent, this, args):
    # Upstream predictor: 3602
    e = Env(parent)
    e.declare(['id'])
    e.local['arguments'] = Array(args)
    e.set('id', binary('+', '_', call(get(call(get(call(e['$'], this), 'find'), 'value > *'), 'text'))))
    if truth(call(get(get(e['save'], 'objects'), 'hasOwnProperty'), e['id'])):
        put(get(e['save'], 'donatedItems'), get(get(get(e['save'], 'objects'), e['id']), 'name'), 1)
    return U


def callback_17(parent, this, args):
    # Upstream predictor: 3600
    e = Env(parent)
    e.declare([])
    e.local['arguments'] = Array(args)
    if truth(binary('===', call(get(call(e['$'], this), 'attr'), binary('+', get(e['save'], 'ns_prefix'), ':type')), 'LibraryMuseum')):
        call(get(call(get(call(e['$'], this), 'find'), 'museumPieces > item'), 'each'), Fn(callback_18, e))
    return U


def callback_21(parent, this, args):
    # Upstream predictor: 3618
    e = Env(parent)
    e.declare([])
    e.local['arguments'] = Array(args)
    if truth(binary('===', call(get(call(e['$'], this), 'attr'), binary('+', get(e['save'], 'ns_prefix'), ':type')), 'Child')):
        update_env(e, 'child_count', 1, False)
    return U


def callback_20(parent, this, args):
    # Upstream predictor: 3617
    e = Env(parent)
    e.declare([])
    e.local['arguments'] = Array(args)
    call(get(call(get(call(e['$'], this), 'find'), 'characters > NPC'), 'each'), Fn(callback_21, e))
    return U


def callback_22(parent, this, args):
    # Upstream predictor: 3632
    e = Env(parent)
    e.declare(['id'])
    e.local['arguments'] = Array(args)
    e.set('id', call(get(call(e['$'], this), 'text')))
    if truth(binary('===', e['id'], 'ccCraftsRoom')):
        put(e['save'], 'quarryUnlocked', True)
    else:
        if truth(binary('===', e['id'], 'ccPantry')):
            put(e['save'], 'greenhouseUnlocked', True)
        else:
            if truth(binary('===', e['id'], 'ccVault')):
                put(e['save'], 'desertUnlocked', True)
            else:
                if truth(binary('===', e['id'], 'ccMovieTheater')):
                    e.set('sawTheater', True)
                else:
                    if truth(binary('===', e['id'], 'ccMovieTheaterJoja')):
                        e.set('sawJojaTheater', True)
                    else:
                        if truth(binary('===', e['id'], 'HasSpecialCharm')):
                            put(e['save'], 'hasSpecialCharm', True)
                        else:
                            if truth(binary('===', e['id'], 'GotMysteryBook')):
                                put(e['save'], 'gotMysteryBook', True)
                            else:
                                if truth(binary('===', e['id'], 'leoMoved')):
                                    put(e['save'], 'leoMoved', True)
    return U


def callback_24(parent, this, args):
    # Upstream predictor: 3661
    e = Env(parent)
    e.declare(['id'])
    e.local['arguments'] = Array(args)
    e.set('id', call(get(call(get(call(e['$'], this), 'find'), 'key > string'), 'text')))
    if truth(binary('===', e['id'], 'Furnace')):
        put(e['save'], 'hasFurnaceRecipe', True)
    return U


def callback_25(parent, this, args):
    # Upstream predictor: 3668
    e = Env(parent)
    e.declare([])
    e.local['arguments'] = Array(args)
    if truth(binary('===', call(get(call(e['$'], this), 'text')), '191393')):
        put(e['save'], 'ccComplete', True)
    else:
        if truth(binary('===', call(get(call(e['$'], this), 'text')), '502261')):
            put(e['save'], 'jojaComplete', True)
    return U


def callback_26(parent, this, args):
    # Upstream predictor: 3701
    e = Env(parent)
    e.declare(['status', 'who'])
    e.local['arguments'] = Array(args)
    e.set('who', call(get(call(get(call(e['$'], this), 'find'), 'key > string'), 'html')))
    if truth(binary('===', e['who'], 'Krobus')):
        e.set('status', call(get(call(get(call(e['$'], this), 'find'), 'value > Friendship > Status'), 'html')))
        if truth(binary('!==', e['status'], 'Unmet')):
            e.set('includeKrobus', True)
    return U


def callback_29(parent, this, args):
    # Upstream predictor: 3714
    e = Env(parent)
    e.declare(['type', 'who'])
    e.local['arguments'] = Array(args)
    e.set('who', call(get(call(get(call(e['$'], this), 'find'), 'name'), 'html')))
    e.set('type', call(get(call(e['$'], this), 'attr'), binary('+', get(e['save'], 'ns_prefix'), ':type')))
    if truth((_logic30 if truth(_logic30 := call(get(e['ignore'], 'hasOwnProperty'), e['type'])) else call(get(e['ignore'], 'hasOwnProperty'), e['who']))):
        return True
    if truth(binary('===', e['who'], 'Leo')):
        if truth(get(e['save'], 'leoMoved')):
            call(get(get(e['save'], 'characters'), 'push'), e['who'])
    else:
        if truth(binary('===', e['who'], 'Krobus')):
            if truth(e['includeKrobus']):
                call(get(get(e['save'], 'characters'), 'push'), e['who'])
        else:
            if truth(binary('===', e['who'], 'Sandy')):
                if truth(get(e['save'], 'desertUnlocked')):
                    call(get(get(e['save'], 'characters'), 'push'), e['who'])
            else:
                call(get(get(e['save'], 'characters'), 'push'), e['who'])
    return U


def callback_28(parent, this, args):
    # Upstream predictor: 3713
    e = Env(parent)
    e.declare([])
    e.local['arguments'] = Array(args)
    call(get(call(get(call(e['$'], this), 'find'), 'NPC'), 'each'), Fn(callback_29, e))
    return U


def callback_27(parent, this, args):
    # Upstream predictor: 3712
    e = Env(parent)
    e.declare([])
    e.local['arguments'] = Array(args)
    call(get(call(get(call(e['$'], this), 'find'), 'characters'), 'each'), Fn(callback_28, e))
    return U


def callback_31(parent, this, args):
    # Upstream predictor: 3742
    e = Env(parent)
    e.declare(['rules'])
    e.local['arguments'] = Array(args)
    e.set('rules', call(get(call(get(call(e['$'], this), 'find'), 'specialRule'), 'text')))
    if truth(call(get(e['rules'], 'match'), e['beanRegex'])):
        put(e['save'], 'qiCropsActive', True)
        return False
    return U


def parseSummary_8(parent, this, args):
    # Upstream predictor: 173
    e = Env(parent)
    e.declare(['beanRegex', 'child_count', 'dayOfSave', 'farmTypes', 'geodesCracked', 'i', 'ignore', 'includeKrobus', 'mysteryBoxesOpened', 'output', 'rng', 'sawJojaTheater', 'sawTheater', 'share_URL', 'spouse', 'ticketPrizesClaimed', 'timesEnchanted', 'trashCansChecked', 'wasChanged'])
    e.local['arguments'] = Array(args)
    e.local['xmlDoc'] = (args[0] if len(args) > 0 and args[0] is not U else U)
    e.set('output', '')
    e.set('farmTypes', Obj({'0': 'Standard', '1': 'Riverland', '2': 'Forest', '3': 'Hill-top', '4': 'Wilderness', '5': 'Four Corners', '6': 'Beach', 'MeadowlandsFarm': 'Meadowlands'}))
    put(e['save'], 'seasonNames', Array(['Spring', 'Summer', 'Fall', 'Winter']))
    put(e['save'], 'dayNames', Array(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']))
    put(e['save'], 'cartItems', table(0))
    put(e['save'], 'cartItems_1_4', table(1))
    put(e['save'], 'cartFurniture', table(2))
    put(e['save'], 'geodeContents', table(3))
    put(e['save'], 'wallpaperEquiv', table(4))
    put(e['save'], 'weapons', table(5))
    put(e['save'], 'boots', table(6))
    put(e['save'], 'objects', table(7))
    put(e['save'], 'furniture', table(8))
    put(e['save'], 'shirts', table(9))
    put(e['save'], 'version', '1.6')
    put(e['save'], 'farmName', 'Unknown Farm')
    put(e['save'], 'niceDate', '')
    put(e['save'], 'gameID', None)
    put(e['save'], 'daysPlayed', 1)
    put(e['save'], 'year', 1)
    put(e['save'], 'geodesCracked', Array([0]))
    put(e['save'], 'mysteryBoxesOpened', Array([0]))
    put(e['save'], 'ticketPrizesClaimed', Array([0]))
    put(e['save'], 'timesEnchanted', Array([0]))
    put(e['save'], 'trashCansChecked', Array([0]))
    put(e['save'], 'deepestMineLevel', 0)
    put(e['save'], 'timesFedRaccoons', 0)
    put(e['save'], 'dailyLuck', unary('-', 0.1))
    put(e['save'], 'luckLevel', 0)
    put(e['save'], 'canHaveChildren', False)
    put(e['save'], 'quarryUnlocked', False)
    put(e['save'], 'desertUnlocked', False)
    put(e['save'], 'greenhouseUnlocked', False)
    put(e['save'], 'theaterUnlocked', False)
    put(e['save'], 'ccComplete', False)
    put(e['save'], 'jojaComplete', False)
    put(e['save'], 'hasFurnaceRecipe', False)
    put(e['save'], 'hasSpecialCharm', False)
    put(e['save'], 'leoMoved', False)
    put(e['save'], 'hasGarbageBook', False)
    put(e['save'], 'gotMysteryBook', False)
    put(e['save'], 'useLegacyRandom', False)
    put(e['save'], 'hardmodeMines', False)
    put(e['save'], 'qiCropsActive', False)
    put(e['save'], 'visitsUntilY1Guarantee', unary('-', 1))
    put(e['save'], 'names', Array([]))
    put(e['save'], 'gender', Array([]))
    put(e['save'], 'characters', table(10))
    put(e['save'], 'donatedItems', table(11))
    put(e['save'], 'dayAdjust', 0)
    if truth(binary('!==', unary('typeof', e['xmlDoc']), 'undefined')):
        put(e['save'], 'gameID', call(e['Number'], call(get(call(get(call(e['$'], e['xmlDoc']), 'find'), 'uniqueIDForThisGame'), 'text'))))
        put(e['save'], 'version', call(get(call(get(call(get(call(e['$'], e['xmlDoc']), 'find'), 'gameVersion'), 'first')), 'text')))
        if truth(binary('===', get(e['save'], 'version'), '')):
            put(e['save'], 'version', '1.2')
            if truth(binary('===', call(get(call(get(call(e['$'], e['xmlDoc']), 'find'), 'hasApplied1_4_UpdateChanges'), 'text')), 'true')):
                put(e['save'], 'version', '1.4')
            else:
                if truth(binary('===', call(get(call(get(call(e['$'], e['xmlDoc']), 'find'), 'hasApplied1_3_UpdateChanges'), 'text')), 'true')):
                    put(e['save'], 'version', '1.3')
        if truth(binary('>=', call(e['compareSemVer'], get(e['save'], 'version'), '1.3'), 0)):
            call(get(call(e['$'], '#cart-title'), 'html'), 'Traveling Merchant Cart and Night Market Boat')
        else:
            call(get(call(e['$'], '#cart-title'), 'html'), 'Traveling Merchant Cart')
        put(e['save'], 'ns_prefix', ('xsi' if truth(binary('>', get(call(get(call(e['$'], e['xmlDoc']), 'find'), 'SaveGame[xmlns\\:xsi]'), 'length'), 0)) else 'p3'))
        put(e['save'], 'mp_ids', Array([]))
        put(e['save'], 'geodesCracked', Array([]))
        put(e['save'], 'mysteryBoxesOpened', Array([]))
        put(e['save'], 'ticketPrizesClaimed', Array([]))
        put(e['save'], 'timesEnchanted', Array([]))
        put(e['save'], 'trashCansChecked', Array([]))
        put(e['save'], 'visitsUntilY1Guarantee', call(e['Number'], call(get(call(get(call(e['$'], e['xmlDoc']), 'find'), 'SaveGame > visitsUntilY1Guarantee'), 'text'))))
        put(e['save'], 'farmName', binary('+', binary('+', binary('+', call(get(call(get(call(e['$'], e['xmlDoc']), 'find'), 'SaveGame > player > farmName'), 'html')), ' Farm ('), get(e['farmTypes'], call(get(call(get(call(e['$'], e['xmlDoc']), 'find'), 'whichFarm'), 'text')))), ')'))
        call(get(get(e['save'], 'names'), 'push'), call(get(call(get(call(e['$'], e['xmlDoc']), 'find'), 'SaveGame > player > name'), 'html')))
        call(get(get(e['save'], 'gender'), 'push'), call(get(call(get(call(e['$'], e['xmlDoc']), 'find'), 'SaveGame > player > gender'), 'text')))
        if truth(binary('>=', call(e['compareSemVer'], get(e['save'], 'version'), '1.3'), 0)):
            call(get(get(e['save'], 'mp_ids'), 'push'), call(e['bigInt'], call(get(call(get(call(e['$'], e['xmlDoc']), 'find'), 'SaveGame > player > UniqueMultiplayerID'), 'text'))))
        if truth(binary('>=', call(e['compareSemVer'], get(e['save'], 'version'), '1.6'), 0)):
            e.set('geodesCracked', 0)
            e.set('mysteryBoxesOpened', 0)
            e.set('ticketPrizesClaimed', 0)
            e.set('timesEnchanted', 0)
            e.set('trashCansChecked', 0)
            call(get(call(get(call(e['$'], e['xmlDoc']), 'find'), 'SaveGame > player > stats > Values > item'), 'each'), Fn(callback_9, e))
            call(get(get(e['save'], 'geodesCracked'), 'push'), e['geodesCracked'])
            call(get(get(e['save'], 'mysteryBoxesOpened'), 'push'), e['mysteryBoxesOpened'])
            call(get(get(e['save'], 'ticketPrizesClaimed'), 'push'), e['ticketPrizesClaimed'])
            call(get(get(e['save'], 'timesEnchanted'), 'push'), e['timesEnchanted'])
            call(get(get(e['save'], 'trashCansChecked'), 'push'), e['trashCansChecked'])
            call(get(call(get(call(e['$'], e['xmlDoc']), 'find'), 'farmhands > Farmer'), 'each'), Fn(callback_10, e))
            (put(e['save'], 'timesFedRaccoons', call(e['Number'], call(get(call(get(call(e['$'], e['xmlDoc']), 'find'), 'SaveGame > timesFedRaccoons'), 'text')))), put(e['save'], 'useLegacyRandom', binary('===', call(get(call(get(call(e['$'], e['xmlDoc']), 'find'), 'useLegacyRandom'), 'text')), 'true')))[-1]
            call(get(get(get(e['save'], 'geodeContents'), 275), 'push'), '_Book_Artifact')
        else:
            if truth(binary('>=', call(e['compareSemVer'], get(e['save'], 'version'), '1.3'), 0)):
                call(get(get(e['save'], 'mp_ids'), 'push'), call(e['bigInt'], call(get(call(get(call(e['$'], e['xmlDoc']), 'find'), 'SaveGame > player > UniqueMultiplayerID'), 'text'))))
                call(get(get(e['save'], 'geodesCracked'), 'push'), call(e['Number'], call(get(call(get(call(e['$'], e['xmlDoc']), 'find'), 'SaveGame > player > stats > geodesCracked'), 'text'))))
                call(get(call(get(call(e['$'], e['xmlDoc']), 'find'), 'farmhand'), 'each'), Fn(callback_13, e))
                put(e['save'], 'daysPlayed', call(e['Number'], call(get(call(get(call(get(call(e['$'], e['xmlDoc']), 'find'), 'stats > daysPlayed'), 'first')), 'text'))))
                if truth(binary('>=', call(e['compareSemVer'], get(e['save'], 'version'), '1.4'), 0)):
                    e.set('timesEnchanted', 0)
                    e.set('trashCansChecked', 0)
                    call(get(call(get(call(e['$'], e['xmlDoc']), 'find'), 'SaveGame > player > stats > stat_dictionary > item'), 'each'), Fn(callback_14, e))
                    call(get(get(e['save'], 'timesEnchanted'), 'push'), e['timesEnchanted'])
                    call(get(get(e['save'], 'trashCansChecked'), 'push'), e['trashCansChecked'])
                    call(get(call(get(call(e['$'], e['xmlDoc']), 'find'), 'farmhand'), 'each'), Fn(callback_15, e))
            else:
                call(get(get(e['save'], 'geodesCracked'), 'push'), call(e['Number'], call(get(call(get(call(e['$'], e['xmlDoc']), 'find'), 'SaveGame > stats > geodesCracked'), 'text'))))
                put(e['save'], 'daysPlayed', call(e['Number'], call(get(call(get(call(get(call(e['$'], e['xmlDoc']), 'find'), 'stats > daysPlayed'), 'first')), 'text'))))
        if truth(binary('===', get(get(e['save'], 'trashCansChecked'), 'length'), 0)):
            call(get(get(e['save'], 'trashCansChecked'), 'push'), 0)
        if truth(binary('===', get(get(e['save'], 'timesEnchanted'), 'length'), 0)):
            call(get(get(e['save'], 'timesEnchanted'), 'push'), 0)
        if truth(binary('===', get(get(e['save'], 'mysteryBoxesOpened'), 'length'), 0)):
            call(get(get(e['save'], 'mysteryBoxesOpened'), 'push'), 0)
        put(e['save'], 'year', call(e['Number'], call(get(call(get(call(get(call(e['$'], e['xmlDoc']), 'find'), 'SaveGame > year'), 'first')), 'text'))))
        put(e['save'], 'niceDate', binary('+', binary('+', binary('+', binary('+', binary('+', 'Day ', call(e['Number'], call(get(call(get(call(e['$'], e['xmlDoc']), 'find'), 'SaveGame > dayOfMonth'), 'text')))), ' of '), call(e['capitalize'], call(get(call(get(call(e['$'], e['xmlDoc']), 'find'), 'SaveGame > currentSeason'), 'html')))), ', Year '), get(e['save'], 'year')))
        if truth(binary('>=', call(e['compareSemVer'], get(e['save'], 'version'), '1.5'), 0)):
            put(e['save'], 'hardmodeMines', binary('>', call(e['Number'], call(get(call(get(call(e['$'], e['xmlDoc']), 'find'), 'SaveGame > minesDifficulty'), 'text'))), 0))
        put(e['save'], 'deepestMineLevel', call(e['Number'], call(get(call(get(call(e['$'], e['xmlDoc']), 'find'), 'player > deepestMineLevel'), 'text'))))
        call(get(call(get(call(e['$'], e['xmlDoc']), 'find'), 'locations > GameLocation'), 'each'), Fn(callback_17, e))
        put(e['save'], 'canHaveChildren', False)
        if truth(binary('<', call(e['compareSemVer'], get(e['save'], 'version'), '1.3'), 0)):
            e.set('spouse', call(get(call(get(call(e['$'], e['xmlDoc']), 'find'), 'player > spouse'), 'text')))
            e.set('child_count', 0)
            if truth((binary('!==', e['spouse'], '') if truth(_logic19 := binary('!==', unary('typeof', e['spouse']), 'undefined')) else _logic19)):
                call(get(call(get(call(e['$'], e['xmlDoc']), 'find'), 'locations > GameLocation'), 'each'), Fn(callback_20, e))
                if truth(binary('<', e['child_count'], 2)):
                    put(e['save'], 'canHaveChildren', True)
        e.set('sawTheater', False)
        e.set('sawJojaTheater', False)
        call(get(call(get(call(e['$'], e['xmlDoc']), 'find'), 'player > mailReceived > string'), 'each'), Fn(callback_22, e))
        put(e['save'], 'theaterUnlocked', (unary('!', e['sawJojaTheater']) if truth(_logic23 := e['sawTheater']) else _logic23))
        if truth(binary('<', call(e['compareSemVer'], get(e['save'], 'version'), '1.6'), 0)):
            if truth(binary('===', call(get(call(get(call(e['$'], e['xmlDoc']), 'find'), 'player > hasSpecialCharm'), 'text')), 'true')):
                put(e['save'], 'hasSpecialCharm', True)
        call(get(call(get(call(e['$'], e['xmlDoc']), 'find'), 'player > craftingRecipes > item'), 'each'), Fn(callback_24, e))
        call(get(call(get(call(e['$'], e['xmlDoc']), 'find'), 'player > eventsSeen > *'), 'each'), Fn(callback_25, e))
        e.set('includeKrobus', False)
        e.set('ignore', table(12))
        call(get(call(get(call(e['$'], e['xmlDoc']), 'find'), 'player > friendshipData > item'), 'each'), Fn(callback_26, e))
        put(e['save'], 'characters', Array([]))
        call(get(call(get(call(e['$'], e['xmlDoc']), 'find'), 'locations > GameLocation'), 'each'), Fn(callback_27, e))
        if truth(binary('>=', call(e['compareSemVer'], get(e['save'], 'version'), '1.5'), 0)):
            e.set('beanRegex', Regex('DROP_QI_BEANS', ''))
            call(get(call(get(call(e['$'], e['xmlDoc']), 'find'), 'SaveGame > specialOrders > SpecialOrder'), 'each'), Fn(callback_31, e))
    e.set('wasChanged', Obj({}))
    put(e['wasChanged'], 'version', call(e['overrideSaveData'], 'version', 'version', 'v', 'text'))
    put(e['wasChanged'], 'gameID', call(e['overrideSaveData'], 'gameID', 'gameID', 'id', 'bigint'))
    put(e['wasChanged'], 'dayAdjust', call(e['overrideSaveData'], 'dayAdjust', 'dayAdjust', 'da', 'int'))
    put(e['wasChanged'], 'daysPlayed', call(e['overrideSaveData'], 'daysPlayed', 'daysPlayed', 'dp', 'int'))
    if truth((_logic32 if truth(_logic32 := binary('>', get(e['save'], 'dayAdjust'), 0)) else get(e['wasChanged'], 'daysPlayed'))):
        put(e['save'], 'year', binary('+', 1, call(get(e['Math'], 'floor'), binary('/', binary('+', get(e['save'], 'daysPlayed'), get(e['save'], 'dayAdjust')), 112))))
        put(e['save'], 'niceDate', '')
    put(e['wasChanged'], 'geodesCracked', call(e['overrideSaveData'], 'geodesCracked', 'geodesCracked', 'gc', 'array'))
    put(e['wasChanged'], 'mysteryBoxesOpened', call(e['overrideSaveData'], 'mysteryBoxesOpened', 'mysteryBoxesOpened', 'mb', 'array'))
    put(e['wasChanged'], 'ticketPrizesClaimed', call(e['overrideSaveData'], 'ticketPrizesClaimed', 'ticketPrizesClaimed', 'pt', 'array'))
    put(e['wasChanged'], 'timesEnchanted', call(e['overrideSaveData'], 'timesEnchanted', 'timesEnchanted', 'te', 'array'))
    put(e['wasChanged'], 'trashCansChecked', call(e['overrideSaveData'], 'trashCansChecked', 'trashCansChecked', 'tc', 'array'))
    put(e['wasChanged'], 'deepestMineLevel', call(e['overrideSaveData'], 'deepestMineLevel', 'deepestMineLevel', 'dml', 'int'))
    put(e['wasChanged'], 'timesFedRaccoons', call(e['overrideSaveData'], 'timesFedRaccoons', 'timesFedRaccoons', 'tfr', 'int'))
    put(e['wasChanged'], 'visitsUntilY1Guarantee', call(e['overrideSaveData'], 'visitsUntilY1Guarantee', 'visitsUntilY1Guarantee', 'vg', 'int'))
    put(e['wasChanged'], 'dailyLuck', call(e['overrideSaveData'], 'dailyLuck', 'dailyLuck', 'dl', 'num'))
    put(e['wasChanged'], 'luckLevel', call(e['overrideSaveData'], 'luckLevel', 'luckLevel', 'll', 'int'))
    put(e['wasChanged'], 'canHaveChildren', call(e['overrideSaveData'], 'canHaveChildren', 'canHaveChildren', 'chc', 'bool'))
    put(e['wasChanged'], 'quarryUnlocked', call(e['overrideSaveData'], 'quarryUnlocked', 'quarryUnlocked', 'qu', 'bool'))
    put(e['wasChanged'], 'desertUnlocked', call(e['overrideSaveData'], 'desertUnlocked', 'desertUnlocked', 'du', 'bool'))
    put(e['wasChanged'], 'greenhouseUnlocked', call(e['overrideSaveData'], 'greenhouseUnlocked', 'greenhouseUnlocked', 'gu', 'bool'))
    put(e['wasChanged'], 'hasFurnaceRecipe', call(e['overrideSaveData'], 'hasFurnaceRecipe', 'hasFurnaceRecipe', 'hfr', 'bool'))
    put(e['wasChanged'], 'hasSpecialCharm', call(e['overrideSaveData'], 'hasSpecialCharm', 'hasSpecialCharm', 'hsc', 'bool'))
    put(e['wasChanged'], 'leoMoved', call(e['overrideSaveData'], 'leoMoved', 'leoMoved', 'leo', 'bool'))
    put(e['wasChanged'], 'hasGarbageBook', call(e['overrideSaveData'], 'hasGarbageBook', 'hasGarbageBook', 'hgb', 'bool'))
    put(e['wasChanged'], 'gotMysteryBook', call(e['overrideSaveData'], 'gotMysteryBook', 'gotMysteryBook', 'gmb', 'bool'))
    put(e['wasChanged'], 'hardmodeMines', call(e['overrideSaveData'], 'hardmodeMines', 'hardmodeMines', 'hm', 'bool'))
    put(e['wasChanged'], 'useLegacyRandom', call(e['overrideSaveData'], 'useLegacyRandom', 'useLegacyRandom', 'leg', 'bool'))
    put(e['wasChanged'], 'theaterUnlocked', call(e['overrideSaveData'], 'theaterUnlocked', 'theaterUnlocked', 'tu', 'bool'))
    put(e['wasChanged'], 'ccComplete', call(e['overrideSaveData'], 'ccComplete', 'ccComplete', 'cc', 'bool'))
    put(e['wasChanged'], 'jojaComplete', call(e['overrideSaveData'], 'jojaComplete', 'jojaComplete', 'jc', 'bool'))
    put(e['wasChanged'], 'qiCropsActive', call(e['overrideSaveData'], 'qiCropsActive', 'qiCropsActive', 'qc', 'bool'))
    put(e['save'], 'originalGuarantee', unary('-', 1))
    if truth(binary('>=', get(e['save'], 'visitsUntilY1Guarantee'), 0)):
        e.set('dayOfSave', binary('+', get(e['save'], 'daysPlayed'), get(e['save'], 'dayAdjust')))
        put(e['save'], 'originalGuarantee', binary('+', binary('+', get(e['save'], 'visitsUntilY1Guarantee'), call(get(e['Math'], 'floor'), binary('/', e['dayOfSave'], 7))), call(get(e['Math'], 'floor'), binary('/', binary('+', e['dayOfSave'], 2), 7))))
        if truth(binary('>=', e['dayOfSave'], 99)):
            update_prop(e['save'], 'originalGuarantee', 1, False)
        if truth(binary('>=', e['dayOfSave'], 100)):
            update_prop(e['save'], 'originalGuarantee', 1, False)
        if truth(binary('>=', e['dayOfSave'], 101)):
            update_prop(e['save'], 'originalGuarantee', 1, False)
    else:
        if truth(binary('==', get(e['save'], 'visitsUntilY1Guarantee'), unary('-', 99))):
            e.set('rng', call(e['CSRandom'], binary('*', 12, get(e['save'], 'gameID'))))
            put(e['save'], 'originalGuarantee', call(get(e['rng'], 'Next'), 2, 31))
    put(e['save'], 'dailyLuck', call(get(e['Math'], 'min'), 0.1, call(get(e['Math'], 'max'), unary('-', 0.1), get(e['save'], 'dailyLuck'))))
    e.set('share_URL', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', get(get(e['window'], 'location'), 'protocol'), '//'), get(get(e['window'], 'location'), 'host')), get(get(e['window'], 'location'), 'pathname')), '?id='), get(e['save'], 'gameID')), '&amp;v='), get(e['save'], 'version')), '&amp;dp='), get(e['save'], 'daysPlayed')), '&amp;dl='), get(e['save'], 'dailyLuck')), '&amp;ll='), get(e['save'], 'luckLevel')), '&amp;dml='), get(e['save'], 'deepestMineLevel')), '&amp;vg='), get(e['save'], 'visitsUntilY1Guarantee')), '&amp;gc='), get(get(e['save'], 'geodesCracked'), 0)), '&amp;mb='), get(get(e['save'], 'mysteryBoxesOpened'), 0)), '&amp;te='), get(get(e['save'], 'timesEnchanted'), 0)), '&amp;tc='), get(get(e['save'], 'trashCansChecked'), 0)), '&amp;pt='), get(get(e['save'], 'ticketPrizesClaimed'), 0)), '&amp;tfr='), get(e['save'], 'timesFedRaccoons')), (binary('+', '&amp;da=', get(e['save'], 'dayAdjust')) if truth(binary('!==', get(e['save'], 'dayAdjust'), 0)) else '')), ('&amp;chc=' if truth(get(e['save'], 'canHaveChildren')) else '')), ('&amp;qu=1' if truth(get(e['save'], 'quarryUnlocked')) else '')), ('&amp;du=1' if truth(get(e['save'], 'desertUnlocked')) else '')), ('&amp;gu=1' if truth(get(e['save'], 'greenhouseUnlocked')) else '')), ('&amp;cc=1' if truth(get(e['save'], 'ccComplete')) else '')), ('&amp;jc=1' if truth(get(e['save'], 'jojaComplete')) else '')), ('&amp;tu=1' if truth(get(e['save'], 'theaterUnlocked')) else '')), ('&amp;hfr=1' if truth(get(e['save'], 'hasFurnaceRecipe')) else '')), ('&amp;hsc=1' if truth(get(e['save'], 'hasSpecialCharm')) else '')), ('&amp;leo=1' if truth(get(e['save'], 'leoMoved')) else '')), ('&amp;hgb=1' if truth(get(e['save'], 'hasGarbageBook')) else '')), ('&amp;gmb=1' if truth(get(e['save'], 'gotMysteryBook')) else '')), ('&amp;hm=1' if truth(get(e['save'], 'hardmodeMines')) else '')), ('&amp;qc=1' if truth(get(e['save'], 'qiCropsActive')) else '')), ('&amp;leg=1' if truth(get(e['save'], 'useLegacyRandom')) else '')))
    call(get(call(e['$'], '#share_URL'), 'html'), binary('+', binary('+', binary('+', binary('+', '<a href="', e['share_URL']), '">'), e['share_URL']), '</a>'))
    if truth(binary('<', call(e['compareSemVer'], get(e['save'], 'version'), '1.1'), 0)):
        put(get(get(e['save'], 'objects'), '_424'), 'price', 160)
        put(get(get(e['save'], 'objects'), '_426'), 'price', 300)
        put(get(get(e['save'], 'objects'), '_444'), 'price', 100)
    else:
        if truth(binary('<', call(e['compareSemVer'], get(e['save'], 'version'), '1.4'), 0)):
            put(get(get(e['save'], 'objects'), '_424'), 'price', 200)
            put(get(get(e['save'], 'objects'), '_426'), 'price', 375)
        else:
            if truth(binary('<', call(e['compareSemVer'], get(e['save'], 'version'), '1.5'), 0)):
                put(get(get(e['save'], 'objects'), '_444'), 'price', 175)
            else:
                if truth(binary('<', call(e['compareSemVer'], get(e['save'], 'version'), '1.6'), 0)):
                    put(get(get(e['save'], 'objects'), '_251'), 'price', 500)
                    put(get(get(e['save'], 'objects'), '_459'), 'price', 200)
                    put(get(get(e['save'], 'objects'), '_773'), 'price', 500)
    if truth(binary('===', get(e['save'], 'gameID'), None)):
        return '<span class="error">Fatal Error: Problem reading save file and no ID passed via query string.</span>'
    e.set('output', binary('+', e['output'], '<h3>Save State Summary</h3><p>Important information taken from the save file which is needed for predictions. Anything that was overridden by <a href="#advanced_usage">a URL parameter</a> is marked with an asterisk (*).</p>'))
    e.set('output', binary('+', e['output'], '<table class="summary"><tr><td>'))
    e.set('output', binary('+', e['output'], binary('+', binary('+', binary('+', binary('+', '<span class="result">', ('*' if truth(get(e['wasChanged'], 'gameID')) else '')), 'Game ID: '), get(e['save'], 'gameID')), '</span><br/>')))
    e.set('output', binary('+', e['output'], binary('+', binary('+', binary('+', binary('+', '<span class="result">', ('*' if truth(get(e['wasChanged'], 'version')) else '')), 'Stardew version: '), get(e['save'], 'version')), '</span><br/>')))
    if truth(binary('===', get(get(e['save'], 'names'), 'length'), 0)):
        put(get(e['save'], 'names'), 0, 'Unknown Farmer')
    e.set('output', binary('+', e['output'], binary('+', binary('+', binary('+', binary('+', '<span class="result">Farmer ', get(get(e['save'], 'names'), 0)), ' of '), get(e['save'], 'farmName')), '</span><br/>')))
    if truth(binary('>', get(get(e['save'], 'names'), 'length'), 1)):
        e.set('output', binary('+', e['output'], binary('+', binary('+', '<span class="result">Farmhands: ', call(get(call(get(get(e['save'], 'names'), 'slice'), 1), 'join'), ', ')), '</span><br/>')))
    if truth(binary('!==', get(e['save'], 'niceDate'), '')):
        e.set('output', binary('+', e['output'], binary('+', binary('+', binary('+', binary('+', '<span class="result">', get(e['save'], 'niceDate')), ' ('), get(e['save'], 'daysPlayed')), ' days played)</span><br/>\n')))
    else:
        e.set('output', binary('+', e['output'], binary('+', binary('+', binary('+', '<span class="result">', ('*' if truth((_logic33 if truth(_logic33 := get(e['wasChanged'], 'daysPlayed')) else get(e['wasChanged'], 'dayAdjust'))) else '')), binary('+', get(e['save'], 'daysPlayed'), get(e['save'], 'dayAdjust'))), ' days played</span><br/>\n')))
    e.set('output', binary('+', e['output'], binary('+', binary('+', '<span class="result">', ('*' if truth(get(e['wasChanged'], 'geodesCracked')) else '')), 'Geodes cracked: ')))
    e.set('i', 0)
    while truth(binary('<', e['i'], get(get(e['save'], 'names'), 'length'))):
        e.set('output', binary('+', e['output'], binary('+', binary('+', binary('+', get(get(e['save'], 'geodesCracked'), e['i']), ' ('), get(get(e['save'], 'names'), e['i'])), ') ')))
        update_env(e, 'i', 1, False)
    e.set('output', binary('+', e['output'], '</span><br/>'))
    if truth(binary('>=', call(e['compareSemVer'], get(e['save'], 'version'), '1.6'), 0)):
        e.set('output', binary('+', e['output'], binary('+', binary('+', '<span class="result">', ('*' if truth(get(e['wasChanged'], 'mysteryBoxesOpened')) else '')), 'Mystery Boxes opened: ')))
        e.set('i', 0)
        while truth(binary('<', e['i'], get(get(e['save'], 'names'), 'length'))):
            e.set('output', binary('+', e['output'], binary('+', binary('+', binary('+', get(get(e['save'], 'mysteryBoxesOpened'), e['i']), ' ('), get(get(e['save'], 'names'), e['i'])), ') ')))
            update_env(e, 'i', 1, False)
        e.set('output', binary('+', e['output'], '</span><br/>'))
        e.set('output', binary('+', e['output'], binary('+', binary('+', '<span class="result">', ('*' if truth(get(e['wasChanged'], 'ticketPrizesClaimed')) else '')), 'Prize Tickets claimed: ')))
        e.set('i', 0)
        while truth(binary('<', e['i'], get(get(e['save'], 'names'), 'length'))):
            e.set('output', binary('+', e['output'], binary('+', binary('+', binary('+', get(get(e['save'], 'ticketPrizesClaimed'), e['i']), ' ('), get(get(e['save'], 'names'), e['i'])), ') ')))
            update_env(e, 'i', 1, False)
        e.set('output', binary('+', e['output'], '</span><br/>'))
    if truth(binary('>=', call(e['compareSemVer'], get(e['save'], 'version'), '1.5'), 0)):
        e.set('output', binary('+', e['output'], binary('+', binary('+', '<span class="result">', ('*' if truth(get(e['wasChanged'], 'timesEnchanted')) else '')), 'Times enchanted: ')))
        e.set('i', 0)
        while truth(binary('<', e['i'], get(get(e['save'], 'names'), 'length'))):
            e.set('output', binary('+', e['output'], binary('+', binary('+', binary('+', get(get(e['save'], 'timesEnchanted'), e['i']), ' ('), get(get(e['save'], 'names'), e['i'])), ') ')))
            update_env(e, 'i', 1, False)
        e.set('output', binary('+', e['output'], '</span><br/>'))
    e.set('output', binary('+', e['output'], binary('+', binary('+', '<span class="result">', ('*' if truth(get(e['wasChanged'], 'trashCansChecked')) else '')), 'Trash cans checked: ')))
    e.set('i', 0)
    while truth(binary('<', e['i'], get(get(e['save'], 'names'), 'length'))):
        e.set('output', binary('+', e['output'], binary('+', binary('+', binary('+', get(get(e['save'], 'trashCansChecked'), e['i']), ' ('), get(get(e['save'], 'names'), e['i'])), ') ')))
        update_env(e, 'i', 1, False)
    e.set('output', binary('+', e['output'], '</span><br/>'))
    e.set('output', binary('+', e['output'], binary('+', binary('+', binary('+', binary('+', '<span class="result">', ('*' if truth(get(e['wasChanged'], 'deepestMineLevel')) else '')), 'Deepest mine level: '), call(get(e['Math'], 'min'), 120, get(e['save'], 'deepestMineLevel'))), '</span><br/>')))
    e.set('output', binary('+', e['output'], binary('+', binary('+', binary('+', binary('+', '<span class="result">', ('*' if truth(get(e['wasChanged'], 'timesFedRaccoons')) else '')), 'Times fed raccoons: '), get(e['save'], 'timesFedRaccoons')), '</span><br/>')))
    e.set('output', binary('+', e['output'], binary('+', binary('+', '<span class="result">', ('*' if truth(get(e['wasChanged'], 'visitsUntilY1Guarantee')) else '')), 'Cart Y1 Guarantee: ')))
    if truth(binary('>=', get(e['save'], 'visitsUntilY1Guarantee'), 0)):
        e.set('output', binary('+', e['output'], binary('+', get(e['save'], 'visitsUntilY1Guarantee'), ' visits left')))
    else:
        if truth(binary('>', get(e['save'], 'originalGuarantee'), 0)):
            e.set('output', binary('+', e['output'], binary('+', get(e['save'], 'originalGuarantee'), ' visits originally rolled')))
        else:
            e.set('output', binary('+', e['output'], ' not active or already past'))
    e.set('output', binary('+', e['output'], '</span><br/>'))
    e.set('output', binary('+', e['output'], binary('+', binary('+', binary('+', '<span class="result">', ('*' if truth(get(e['wasChanged'], 'dailyLuck')) else '')), 'Daily Luck is assumed to be '), get(e['save'], 'dailyLuck'))))
    if truth(get(e['save'], 'hasSpecialCharm')):
        put(e['save'], 'dailyLuck', binary('+', get(e['save'], 'dailyLuck'), 0.025))
        e.set('output', binary('+', e['output'], binary('+', binary('+', ' (', call(get(get(e['save'], 'dailyLuck'), 'toFixed'), 3)), ' with charm)')))
    e.set('output', binary('+', e['output'], '</span><br/>'))
    e.set('output', binary('+', e['output'], binary('+', binary('+', binary('+', binary('+', '<span class="result">', ('*' if truth(get(e['wasChanged'], 'luckLevel')) else '')), 'Luck buffs are assumed to be '), get(e['save'], 'luckLevel')), '</span><br/>')))
    e.set('output', binary('+', e['output'], '</td><td>'))
    e.set('output', binary('+', e['output'], binary('+', binary('+', binary('+', binary('+', '<span class="result">', ('*' if truth(get(e['wasChanged'], 'useLegacyRandom')) else '')), 'Legacy RNG Seeding is '), ('on' if truth(get(e['save'], 'useLegacyRandom')) else 'off')), '</span><br/>')))
    e.set('output', binary('+', e['output'], binary('+', binary('+', binary('+', binary('+', '<span class="result">', ('*' if truth(get(e['wasChanged'], 'quarryUnlocked')) else '')), 'Quarry is '), ('' if truth(get(e['save'], 'quarryUnlocked')) else 'not')), ' unlocked</span><br/>')))
    e.set('output', binary('+', e['output'], binary('+', binary('+', binary('+', binary('+', '<span class="result">', ('*' if truth(get(e['wasChanged'], 'desertUnlocked')) else '')), 'Desert is '), ('' if truth(get(e['save'], 'desertUnlocked')) else 'not')), ' unlocked</span><br/>')))
    e.set('output', binary('+', e['output'], binary('+', binary('+', binary('+', binary('+', '<span class="result">', ('*' if truth(get(e['wasChanged'], 'greenhouseUnlocked')) else '')), 'Greenhouse is '), ('' if truth(get(e['save'], 'greenhouseUnlocked')) else 'not')), ' unlocked</span><br/>')))
    e.set('output', binary('+', e['output'], binary('+', binary('+', binary('+', binary('+', '<span class="result">', ('*' if truth(get(e['wasChanged'], 'ccComplete')) else '')), 'Community Center is '), ('' if truth(get(e['save'], 'ccComplete')) else 'not')), ' complete</span><br/>')))
    e.set('output', binary('+', e['output'], binary('+', binary('+', binary('+', binary('+', '<span class="result">', ('*' if truth(get(e['wasChanged'], 'jojaComplete')) else '')), 'Joja Community Development is '), ('' if truth(get(e['save'], 'jojaComplete')) else 'not')), ' complete</span><br/>')))
    e.set('output', binary('+', e['output'], binary('+', binary('+', binary('+', binary('+', '<span class="result">', ('*' if truth(get(e['wasChanged'], 'theaterUnlocked')) else '')), 'Theater is '), ('' if truth(get(e['save'], 'theaterUnlocked')) else 'not')), ' unlocked</span><br/>')))
    if truth(binary('<', call(e['compareSemVer'], get(e['save'], 'version'), '1.3'), 0)):
        e.set('output', binary('+', e['output'], binary('+', binary('+', binary('+', binary('+', '<span class="result">', ('*' if truth(get(e['wasChanged'], 'canHaveChildren')) else '')), 'Farmer can'), ('' if truth(get(e['save'], 'canHaveChildren')) else 'not')), ' have more children</span><br/>')))
    e.set('output', binary('+', e['output'], binary('+', binary('+', binary('+', binary('+', '<span class="result">', ('*' if truth(get(e['wasChanged'], 'hasFurnaceRecipe')) else '')), 'Farmer '), ('has' if truth(get(e['save'], 'hasFurnaceRecipe')) else 'does not have')), ' furnace recipe</span><br/>')))
    e.set('output', binary('+', e['output'], binary('+', binary('+', binary('+', binary('+', '<span class="result">', ('*' if truth(get(e['wasChanged'], 'hasSpecialCharm')) else '')), 'Farmer '), ('has' if truth(get(e['save'], 'hasSpecialCharm')) else 'does not have')), ' special luck charm</span><br/>')))
    e.set('output', binary('+', e['output'], binary('+', binary('+', binary('+', binary('+', '<span class="result">', ('*' if truth(get(e['wasChanged'], 'hasGarbageBook')) else '')), 'Farmer has '), ('' if truth(get(e['save'], 'hasGarbageBook')) else 'not')), ' read <span class="book">The Alleyway Buffet</span></span><br/>')))
    e.set('output', binary('+', e['output'], binary('+', binary('+', binary('+', binary('+', '<span class="result">', ('*' if truth(get(e['wasChanged'], 'gotMysteryBook')) else '')), 'Farmer has '), ('' if truth(get(e['save'], 'gotMysteryBook')) else 'not')), ' gotten <span class="book">Mystery Book</span> from Mystery Boxes</span><br/>')))
    e.set('output', binary('+', e['output'], binary('+', binary('+', binary('+', binary('+', '<span class="result">', ('*' if truth(get(e['wasChanged'], 'leoMoved')) else '')), 'Leo has '), ('' if truth(get(e['save'], 'leoMoved')) else 'not')), ' moved to the Valley</span><br/>')))
    e.set('output', binary('+', e['output'], binary('+', binary('+', binary('+', binary('+', '<span class="result">', ('*' if truth(get(e['wasChanged'], 'hardmodeMines')) else '')), 'Mines are '), ('' if truth(get(e['save'], 'hardmodeMines')) else 'not')), ' currently hard difficulty</span><br/>')))
    e.set('output', binary('+', e['output'], binary('+', binary('+', binary('+', binary('+', '<span class="result">', ('*' if truth(get(e['wasChanged'], 'qiCropsActive')) else '')), 'Qi Crops special order is '), ('' if truth(get(e['save'], 'qiCropsActive')) else 'not')), ' active</span><br/>')))
    e.set('output', binary('+', e['output'], '</td></tr></table>'))
    return e['output']
    return U


def predictMines_34(parent, this, args):
    # Upstream predictor: 3993
    e = Env(parent)
    e.declare(['day', 'dinoLevel', 'dinoText', 'infestedMonster', 'infestedQuarryLevel', 'infestedSlime', 'infestedText', 'mineLevel', 'month', 'monthName', 'mushroomText', 'output', 'quarryLevel', 'quarryText', 'rainbowLights', 'rng', 'skipMushroomCheck', 'slimeText', 'tclass', 'week', 'weekDay', 'year'])
    e.local['arguments'] = Array(args)
    e.local['isSearch'] = (args[0] if len(args) > 0 and args[0] is not U else U)
    e.local['offset'] = (args[1] if len(args) > 1 and args[1] is not U else U)
    e.set('output', '')
    if truth(binary('===', unary('typeof', e['offset']), 'undefined')):
        e.set('offset', binary('*', 28, call(get(e['Math'], 'floor'), binary('/', get(e['save'], 'daysPlayed'), 28))))
    if truth(binary('<', e['offset'], 112)):
        call(get(call(e['$'], '#mines-prev-year'), 'prop'), 'disabled', True)
    else:
        call(get(call(e['$'], '#mines-prev-year'), 'val'), binary('-', e['offset'], 112))
        call(get(call(e['$'], '#mines-prev-year'), 'prop'), 'disabled', False)
    if truth(binary('<', e['offset'], 28)):
        call(get(call(e['$'], '#mines-prev-month'), 'prop'), 'disabled', True)
    else:
        call(get(call(e['$'], '#mines-prev-month'), 'val'), binary('-', e['offset'], 28))
        call(get(call(e['$'], '#mines-prev-month'), 'prop'), 'disabled', False)
    call(get(call(e['$'], '#mines-reset'), 'val'), 'reset')
    call(get(call(e['$'], '#mines-next-month'), 'val'), binary('+', e['offset'], 28))
    call(get(call(e['$'], '#mines-next-year'), 'val'), binary('+', e['offset'], 112))
    e.set('month', call(get(e['Math'], 'floor'), binary('/', e['offset'], 28)))
    e.set('monthName', get(get(e['save'], 'seasonNames'), binary('%', e['month'], 4)))
    e.set('year', binary('+', 1, call(get(e['Math'], 'floor'), binary('/', e['offset'], 112))))
    e.set('output', binary('+', e['output'], binary('+', binary('+', binary('+', binary('+', '<table class="calendar"><thead><tr><th colspan="7">', e['monthName']), ' Year '), e['year']), '</th></tr>\n')))
    e.set('output', binary('+', e['output'], '<tr><th>M</th><th>T</th><th>W</th><th>Th</th><th>F</th><th>Sa</th><th>Su</th></tr></thead>\n<tbody>'))
    e.set('week', 0)
    while truth(binary('<', e['week'], 4)):
        e.set('output', binary('+', e['output'], '<tr>'))
        e.set('weekDay', 1)
        while truth(binary('<', e['weekDay'], 8)):
            e.set('rainbowLights', Array([]))
            e.set('infestedMonster', Array([]))
            e.set('infestedSlime', Array([]))
            e.set('quarryLevel', Array([]))
            e.set('dinoLevel', Array([]))
            e.set('day', binary('+', binary('+', binary('*', 7, e['week']), e['weekDay']), e['offset']))
            if truth(binary('<', call(e['compareSemVer'], get(e['save'], 'version'), '1.4'), 0)):
                e.set('mineLevel', 1)
                while truth(binary('<', e['mineLevel'], 120)):
                    if truth(binary('===', binary('%', e['mineLevel'], 5), 0)):
                        update_env(e, 'mineLevel', 1, False)
                        continue
                    e.set('rng', call(e['CSRandom'], binary('+', binary('+', binary('+', e['day'], get(e['save'], 'dayAdjust')), e['mineLevel']), binary('/', get(e['save'], 'gameID'), 2))))
                    if truth((binary('!==', binary('%', e['mineLevel'], 40), 19) if truth(_logic35 := (binary('<', binary('%', e['mineLevel'], 40), 30) if truth(_logic36 := binary('>', binary('%', e['mineLevel'], 40), 5)) else _logic36)) else _logic35)):
                        if truth(binary('<', call(get(e['rng'], 'NextDouble')), 0.044)):
                            if truth(binary('<', call(get(e['rng'], 'NextDouble')), 0.5)):
                                call(get(e['infestedMonster'], 'push'), e['mineLevel'])
                            else:
                                call(get(e['infestedSlime'], 'push'), e['mineLevel'])
                            update_env(e, 'mineLevel', 1, False)
                            continue
                    e.set('rng', call(e['CSRandom'], binary('+', binary('+', binary('+', e['day'], get(e['save'], 'dayAdjust')), e['mineLevel']), binary('/', get(e['save'], 'gameID'), 2))))
                    if truth((binary('>', e['mineLevel'], 2) if truth(_logic37 := binary('<', call(get(e['rng'], 'NextDouble')), 0.3)) else _logic37)):
                        call(get(e['rng'], 'NextDouble'))
                    call(get(e['rng'], 'NextDouble'))
                    if truth((binary('>', e['mineLevel'], 80) if truth(_logic38 := binary('<', call(get(e['rng'], 'NextDouble')), 0.035)) else _logic38)):
                        call(get(e['rainbowLights'], 'push'), e['mineLevel'])
                    update_env(e, 'mineLevel', 1, False)
                if truth(binary('<', e['day'], get(e['save'], 'daysPlayed'))):
                    e.set('tclass', 'past')
                else:
                    if truth(binary('===', e['day'], get(e['save'], 'daysPlayed'))):
                        e.set('tclass', 'current')
                    else:
                        e.set('tclass', 'future')
            else:
                e.set('mineLevel', 1)
                while truth(binary('<', e['mineLevel'], 120)):
                    e.set('skipMushroomCheck', False)
                    if truth(binary('===', binary('%', e['mineLevel'], 5), 0)):
                        update_env(e, 'mineLevel', 1, False)
                        continue
                    if truth(binary('<', call(e['compareSemVer'], get(e['save'], 'version'), '1.6'), 0)):
                        e.set('rng', call(e['CSRandom'], binary('+', binary('+', binary('+', e['day'], get(e['save'], 'dayAdjust')), binary('*', e['mineLevel'], 100)), binary('/', get(e['save'], 'gameID'), 2))))
                    else:
                        e.set('rng', call(e['CSRandom'], call(e['getRandomSeed'], binary('+', e['day'], get(e['save'], 'dayAdjust')), binary('/', get(e['save'], 'gameID'), 2), binary('*', e['mineLevel'], 100))))
                    if truth((binary('!==', binary('%', e['mineLevel'], 40), 19) if truth(_logic39 := (binary('<', binary('%', e['mineLevel'], 40), 30) if truth(_logic40 := (binary('>', binary('%', e['mineLevel'], 40), 5) if truth(_logic41 := binary('<', call(get(e['rng'], 'NextDouble')), 0.044)) else _logic41)) else _logic40)) else _logic39)):
                        if truth(binary('<', call(get(e['rng'], 'NextDouble')), 0.5)):
                            call(get(e['infestedMonster'], 'push'), e['mineLevel'])
                        else:
                            call(get(e['infestedSlime'], 'push'), e['mineLevel'])
                        e.set('skipMushroomCheck', True)
                    else:
                        if truth((binary('>', binary('%', e['mineLevel'], 40), 1) if truth(_logic42 := (get(e['save'], 'quarryUnlocked') if truth(_logic43 := binary('<', call(get(e['rng'], 'NextDouble')), 0.044)) else _logic43)) else _logic42)):
                            if truth((binary('<', call(e['compareSemVer'], get(e['save'], 'version'), '1.5'), 0) if truth(_logic44 := binary('<', call(get(e['rng'], 'NextDouble')), 0.25)) else _logic44)):
                                call(get(e['quarryLevel'], 'push'), binary('+', e['mineLevel'], '*'))
                            else:
                                call(get(e['quarryLevel'], 'push'), e['mineLevel'])
                            e.set('skipMushroomCheck', True)
                    if truth(e['skipMushroomCheck']):
                        update_env(e, 'mineLevel', 1, False)
                        continue
                    if truth(binary('<', call(e['compareSemVer'], get(e['save'], 'version'), '1.6'), 0)):
                        e.set('rng', call(e['CSRandom'], binary('+', binary('+', binary('*', binary('+', e['day'], get(e['save'], 'dayAdjust')), e['mineLevel']), binary('*', 4, e['mineLevel'])), binary('/', get(e['save'], 'gameID'), 2))))
                    else:
                        e.set('rng', call(e['CSRandom'], call(e['getRandomSeed'], binary('+', e['day'], get(e['save'], 'dayAdjust')), binary('/', get(e['save'], 'gameID'), 2), binary('+', e['day'], get(e['save'], 'dayAdjust')), e['mineLevel'], binary('*', 4, e['mineLevel']))))
                    if truth(unary('!', get(e['save'], 'hardmodeMines'))):
                        if truth((binary('>', e['mineLevel'], 2) if truth(_logic45 := binary('<', call(get(e['rng'], 'NextDouble')), 0.3)) else _logic45)):
                            call(get(e['rng'], 'NextDouble'))
                    call(get(e['rng'], 'NextDouble'))
                    if truth((binary('>', e['mineLevel'], 80) if truth(_logic46 := binary('<', call(get(e['rng'], 'NextDouble')), 0.035)) else _logic46)):
                        call(get(e['rainbowLights'], 'push'), e['mineLevel'])
                    update_env(e, 'mineLevel', 1, False)
                e.set('mineLevel', 127)
                while truth(binary('<', e['mineLevel'], 621)):
                    if truth(binary('<', call(e['compareSemVer'], get(e['save'], 'version'), '1.6'), 0)):
                        e.set('rng', call(e['CSRandom'], binary('+', binary('+', binary('+', e['day'], get(e['save'], 'dayAdjust')), binary('*', e['mineLevel'], 100)), binary('/', get(e['save'], 'gameID'), 2))))
                    else:
                        e.set('rng', call(e['CSRandom'], call(e['getRandomSeed'], binary('+', e['day'], get(e['save'], 'dayAdjust')), binary('/', get(e['save'], 'gameID'), 2), binary('*', e['mineLevel'], 100))))
                    if truth(binary('<', call(get(e['rng'], 'NextDouble')), 0.044)):
                        if truth(binary('<', call(get(e['rng'], 'NextDouble')), 0.5)):
                            pass
                        else:
                            pass
                        if truth(binary('<', call(get(e['rng'], 'NextDouble')), 0.5)):
                            call(get(e['dinoLevel'], 'push'), binary('-', e['mineLevel'], 120))
                    update_env(e, 'mineLevel', 1, False)
                if truth(binary('<', e['day'], get(e['save'], 'daysPlayed'))):
                    e.set('tclass', 'past')
                else:
                    if truth(binary('===', e['day'], get(e['save'], 'daysPlayed'))):
                        e.set('tclass', 'current')
                    else:
                        e.set('tclass', 'future')
            e.set('mushroomText', '<img src="blank.png" class="small-icon" alt="Mushroom" id="icon_m">&nbsp;')
            if truth(binary('===', get(e['rainbowLights'], 'length'), 0)):
                e.set('mushroomText', binary('+', binary('+', '<span class="none">', e['mushroomText']), 'None</span>'))
            else:
                if truth(binary('>', get(e['rainbowLights'], 'length'), 5)):
                    e.set('mushroomText', binary('+', binary('+', binary('+', binary('+', binary('+', '<span data-tooltip="All results: ', e['rainbowLights']), '">'), e['mushroomText']), call(get(call(get(e['rainbowLights'], 'slice'), 0, 4), 'join'), ',&nbsp;')), ',...</span>'))
                else:
                    e.set('mushroomText', binary('+', e['mushroomText'], call(get(e['rainbowLights'], 'join'), ',&nbsp;')))
            e.set('infestedText', '<img src="blank.png" class="small-icon" alt="Sword" id="icon_i">&nbsp;')
            if truth(binary('===', get(e['infestedMonster'], 'length'), 0)):
                e.set('infestedText', binary('+', binary('+', '<span class="none">', e['infestedText']), 'None</span>'))
            else:
                if truth(binary('>', get(e['infestedMonster'], 'length'), 5)):
                    e.set('infestedText', binary('+', binary('+', binary('+', binary('+', binary('+', '<span data-tooltip="All results: ', e['infestedMonster']), '">'), e['infestedText']), call(get(call(get(e['infestedMonster'], 'slice'), 0, 4), 'join'), ',&nbsp;')), ',...</span>'))
                else:
                    e.set('infestedText', binary('+', e['infestedText'], call(get(e['infestedMonster'], 'join'), ',&nbsp;')))
            e.set('slimeText', '<img src="blank.png" class="small-icon" alt="Slime" id="icon_s">&nbsp;')
            if truth(binary('===', get(e['infestedSlime'], 'length'), 0)):
                e.set('slimeText', binary('+', binary('+', '<span class="none">', e['slimeText']), 'None</span>'))
            else:
                if truth(binary('>', get(e['infestedSlime'], 'length'), 5)):
                    e.set('slimeText', binary('+', binary('+', binary('+', binary('+', binary('+', '<span data-tooltip="All results: ', e['infestedSlime']), '">'), e['slimeText']), call(get(call(get(e['infestedSlime'], 'slice'), 0, 4), 'join'), ',&nbsp;')), ',...</span>'))
                else:
                    e.set('slimeText', binary('+', e['slimeText'], call(get(e['infestedSlime'], 'join'), ',&nbsp;')))
            e.set('quarryText', '<img src="blank.png" class="small-icon" alt="Skull" id="icon_q">&nbsp;')
            if truth(binary('===', get(e['quarryLevel'], 'length'), 0)):
                e.set('quarryText', binary('+', binary('+', '<span class="none">', e['quarryText']), 'None</span>'))
            else:
                if truth(binary('>', get(e['quarryLevel'], 'length'), 5)):
                    e.set('quarryText', binary('+', binary('+', binary('+', binary('+', binary('+', '<span data-tooltip="All results: ', e['quarryLevel']), '">'), e['quarryText']), call(get(call(get(e['quarryLevel'], 'slice'), 0, 4), 'join'), ',&nbsp;')), ',...</span>'))
                else:
                    e.set('quarryText', binary('+', e['quarryText'], call(get(e['quarryLevel'], 'join'), ',&nbsp;')))
            e.set('dinoText', '<img src="blank.png" class="small-icon" alt="Dino" id="icon_d">&nbsp;')
            if truth(binary('===', get(e['dinoLevel'], 'length'), 0)):
                e.set('dinoText', binary('+', binary('+', '<span class="none">', e['dinoText']), 'None</span>'))
            else:
                if truth(binary('>', get(e['dinoLevel'], 'length'), 5)):
                    e.set('dinoText', binary('+', binary('+', binary('+', binary('+', binary('+', '<span data-tooltip="All results (level 1-500): ', e['dinoLevel']), '">'), e['dinoText']), call(get(call(get(e['dinoLevel'], 'slice'), 0, 4), 'join'), ',&nbsp;')), ',...</span>'))
                else:
                    e.set('dinoText', binary('+', e['dinoText'], call(get(e['dinoLevel'], 'join'), ',&nbsp;')))
            e.set('output', binary('+', e['output'], binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', '<td class="', e['tclass']), '"><span class="date"> '), binary('-', e['day'], e['offset'])), '</span><br/>'), '<span class="cell">'), e['mushroomText']), '<br/>'), e['infestedText']), '<br/>'), e['slimeText']), '<br/>'), e['quarryText']), '<hr />'), e['dinoText']), '</span></td>')))
            update_env(e, 'weekDay', 1, False)
        e.set('output', binary('+', e['output'], '</tr>\n'))
        update_env(e, 'week', 1, False)
    e.set('output', binary('+', e['output'], '<tr><td colspan="7" class="legend">Regular Mine: <img src="blank.png" class="small-icon" alt="Mushroom" id="icon_m"> Mushroom Level | <img src="blank.png" class="small-icon" alt="Sword" id="icon_i"> Monster Infestation | <img src="blank.png" class="small-icon" alt="Slime" id="icon_s"> Slime Infestation | <img src="blank.png" class="small-icon" alt="Skull" id="icon_q"> Quarry Level (* = Infested; 1.4 only)<br/>Skull Cavern: <img src="blank.png" class="small-icon" alt="Dino" id="icon_d"> Potential Dinosaur Level (not guaranteed)</td></tr>'))
    e.set('output', binary('+', e['output'], '</tbody></table>\n'))
    return e['output']
    return U


def getRandomItemFromSeason_47(parent, this, args):
    # Upstream predictor: 4233
    e = Env(parent)
    e.declare(['possibleItems'])
    e.local['arguments'] = Array(args)
    e.local['rng'] = (args[0] if len(args) > 0 and args[0] is not U else U)
    e.local['season'] = (args[1] if len(args) > 1 and args[1] is not U else U)
    e.set('possibleItems', Array(['Topaz', 'Amethyst', 'Cave Carrot', 'Quartz', 'Earth Crystal', 'Seaweed', 'Joja Cola', 'Green Algae', 'Red Mushroom']))
    if truth(binary('>', get(e['save'], 'deepestMineLevel'), 40)):
        call(get(e['possibleItems'], 'push'), 'Aquamarine', 'Jade', 'Diamond', 'Frozen Tear', 'Purple Mushroom')
    if truth(binary('>', get(e['save'], 'deepestMineLevel'), 80)):
        call(get(e['possibleItems'], 'push'), 'Ruby', 'Emerald', 'Fire Quartz')
    if truth(get(e['save'], 'desertUnlocked')):
        call(get(e['possibleItems'], 'push'), 'Coconut', 'Cactus Fruit', 'Sandfish', 'Scorpion Carp')
    if truth(get(e['save'], 'hasFurnaceRecipe')):
        call(get(e['possibleItems'], 'push'), 'Copper Bar', 'Iron Bar', 'Gold Bar', 'Refined Quartz')
    _switch48 = e['season']
    _switch48_index = -1
    if _switch48_index < 0 and strict_equal(_switch48, 0): _switch48_index = 0
    if _switch48_index < 0 and strict_equal(_switch48, 1): _switch48_index = 1
    if _switch48_index < 0 and strict_equal(_switch48, 2): _switch48_index = 2
    if _switch48_index < 0 and strict_equal(_switch48, 3): _switch48_index = 3
    if _switch48_index < 0: _switch48_index = -1
    while True:
        if 0 <= _switch48_index <= 0:
            call(get(e['possibleItems'], 'push'), 'Wild Horseradish', 'Daffodil', 'Leek', 'Dandelion', 'Anchovy', 'Sardine', 'Bream', 'Largemouth Bass', 'Smallmouth Bass', 'Carp', 'Catfish', 'Sunfish', 'Herring', 'Eel', 'Seaweed', 'Joja Cola', 'Flounder')
            break
        if 0 <= _switch48_index <= 1:
            call(get(e['possibleItems'], 'push'), 'Pufferfish', 'Tuna', 'Bream', 'Largemouth Bass', 'Rainbow Trout', 'Carp', 'Pike', 'Sunfish', 'Red Mullet', 'Octopus', 'Red Snapper', 'Super Cucumber', 'Spice Berry', 'Grape', 'Sweet Pea', 'Flounder')
            break
        if 0 <= _switch48_index <= 2:
            call(get(e['possibleItems'], 'push'), 'Common Mushroom', 'Wild Plum', 'Hazelnut', 'Blackberry', 'Anchovy', 'Sardine', 'Bream', 'Largemouth Bass', 'Smallmouth Bass', 'Salmon', 'Walleye', 'Carp', 'Catfish', 'Eel', 'Red Snapper', 'Sea Cucumber', 'Super Cucumber', 'Midnight Carp')
            break
        if 0 <= _switch48_index <= 3:
            call(get(e['possibleItems'], 'push'), 'Winter Root', 'Crystal Fruit', 'Snow Yam', 'Crocus', 'Tuna', 'Sardine', 'Bream', 'Largemouth Bass', 'Walleye', 'Perch', 'Pike', 'Red Mullet', 'Herring', 'Red Snapper', 'Squid', 'Sea Cucumber', 'Midnight Carp')
            break
        break
    return get(e['possibleItems'], call(get(e['rng'], 'Next'), get(e['possibleItems'], 'length')))
    return U


def predictTrash_49(parent, this, args):
    # Upstream predictor: 4269
    e = Env(parent)
    e.declare(['baseChancePassed', 'canID', 'canList', 'day', 'doubleMega', 'fallbackList', 'goodStuff', 'i', 'luckCheck', 'mega', 'month', 'monthName', 'output', 'prewarm', 'results', 'rng', 'rngSeason', 'rngSynced', 'roll', 'seed', 'stack', 'tclass', 'tileX', 'tileY', 'trashItem', 'trashText', 'week', 'weekDay', 'whichCan', 'year'])
    e.local['arguments'] = Array(args)
    e.local['isSearch'] = (args[0] if len(args) > 0 and args[0] is not U else U)
    e.local['offset'] = (args[1] if len(args) > 1 and args[1] is not U else U)
    e.set('output', '')
    e.set('luckCheck', binary('+', 0.2, get(e['save'], 'dailyLuck')))
    e.set('canList', Array(['Jodi', 'Emily', 'Mayor', 'Museum', 'Clint', 'Saloon', 'George', 'Joja']))
    e.set('canID', Array(['JodiAndKent', 'EmilyAndHaley', 'Mayor', 'Museum', 'Blacksmith', 'Saloon', 'Evelyn', 'JojaMart']))
    e.set('tileX', Array([13, 19, 56, 108, 97, 47, 52, 110]))
    e.set('tileY', Array([86, 89, 85, 91, 80, 70, 63, 56]))
    e.set('fallbackList', Array(['_153', '_216', '_403', '_309', '_310', '_311', 'SEASON', '_168', '_167', '_170', '_171', '_172']))
    if truth(binary('===', unary('typeof', e['offset']), 'undefined')):
        e.set('offset', binary('*', 28, call(get(e['Math'], 'floor'), binary('/', get(e['save'], 'daysPlayed'), 28))))
    if truth(binary('<', e['offset'], 112)):
        call(get(call(e['$'], '#trash-prev-year'), 'prop'), 'disabled', True)
    else:
        call(get(call(e['$'], '#trash-prev-year'), 'val'), binary('-', e['offset'], 112))
        call(get(call(e['$'], '#trash-prev-year'), 'prop'), 'disabled', False)
    if truth(binary('<', e['offset'], 28)):
        call(get(call(e['$'], '#trash-prev-month'), 'prop'), 'disabled', True)
    else:
        call(get(call(e['$'], '#trash-prev-month'), 'val'), binary('-', e['offset'], 28))
        call(get(call(e['$'], '#trash-prev-month'), 'prop'), 'disabled', False)
    call(get(call(e['$'], '#trash-reset'), 'val'), 'reset')
    call(get(call(e['$'], '#trash-next-month'), 'val'), binary('+', e['offset'], 28))
    call(get(call(e['$'], '#trash-next-year'), 'val'), binary('+', e['offset'], 112))
    e.set('month', call(get(e['Math'], 'floor'), binary('/', e['offset'], 28)))
    e.set('monthName', get(get(e['save'], 'seasonNames'), binary('%', e['month'], 4)))
    e.set('year', binary('+', 1, call(get(e['Math'], 'floor'), binary('/', e['offset'], 112))))
    e.set('output', binary('+', e['output'], binary('+', binary('+', binary('+', binary('+', '<table class="calendar"><thead><tr><th colspan="7">', e['monthName']), ' Year '), e['year']), '</th></tr>\n')))
    e.set('output', binary('+', e['output'], '<tr><th>M</th><th>T</th><th>W</th><th>Th</th><th>F</th><th>Sa</th><th>Su</th></tr></thead>\n<tbody>'))
    if truth((get(e['save'], 'hasGarbageBook') if truth(_logic50 := binary('>=', call(e['compareSemVer'], get(e['save'], 'version'), '1.6'), 0)) else _logic50)):
        e.set('luckCheck', binary('+', e['luckCheck'], 0.2))
    e.set('week', 0)
    while truth(binary('<', e['week'], 4)):
        e.set('output', binary('+', e['output'], '<tr>'))
        e.set('weekDay', 1)
        while truth(binary('<', e['weekDay'], 8)):
            e.set('goodStuff', Array([]))
            e.set('day', binary('+', binary('+', binary('*', 7, e['week']), e['weekDay']), e['offset']))
            e.set('whichCan', 0)
            while truth(binary('<', e['whichCan'], 8)):
                if truth(binary('>=', call(e['compareSemVer'], get(e['save'], 'version'), '1.6'), 0)):
                    e.set('seed', call(e['getRandomSeed'], binary('+', e['day'], get(e['save'], 'dayAdjust')), binary('/', get(e['save'], 'gameID'), 2), binary('+', 777, call(e['getHashFromString'], get(e['canID'], e['whichCan'])))))
                else:
                    e.set('seed', binary('+', binary('+', binary('+', binary('+', binary('/', get(e['save'], 'gameID'), 2), e['day']), get(e['save'], 'dayAdjust')), 777), binary('*', e['whichCan'], 77)))
                e.set('rng', call(e['CSRandom'], e['seed']))
                e.set('prewarm', call(get(e['rng'], 'Next'), 0, 100))
                e.set('i', 0)
                while truth(binary('<', e['i'], e['prewarm'])):
                    call(get(e['rng'], 'NextDouble'))
                    update_env(e, 'i', 1, False)
                e.set('prewarm', call(get(e['rng'], 'Next'), 0, 100))
                e.set('i', 0)
                while truth(binary('<', e['i'], e['prewarm'])):
                    call(get(e['rng'], 'NextDouble'))
                    update_env(e, 'i', 1, False)
                e.set('trashItem', '')
                if truth(binary('>=', call(e['compareSemVer'], get(e['save'], 'version'), '1.6'), 0)):
                    e.set('mega', False)
                    e.set('doubleMega', False)
                    e.set('baseChancePassed', binary('<', call(get(e['rng'], 'NextDouble')), e['luckCheck']))
                    if truth((binary('<', call(get(e['rng'], 'NextDouble')), 0.002) if truth(_logic51 := binary('>=', get(get(e['save'], 'trashCansChecked'), 0), 20)) else _logic51)):
                        e.set('doubleMega', True)
                        e.set('trashItem', call(e['wikify'], 'Garbage Hat'))
                    else:
                        if truth((binary('<', call(get(e['rng'], 'NextDouble')), 0.002) if truth(_logic52 := binary('>=', get(get(e['save'], 'trashCansChecked'), 0), 50)) else _logic52)):
                            e.set('doubleMega', True)
                            e.set('trashItem', call(e['wikify'], 'Trash Catalogue'))
                    if truth(binary('===', e['trashItem'], '')):
                        if truth((binary('<', call(get(e['rng'], 'NextDouble')), 0.25) if truth(_logic53 := get(e['save'], 'qiCropsActive')) else _logic53)):
                            e.set('trashItem', call(e['wikify'], 'Qi Bean'))
                        else:
                            if truth(e['baseChancePassed']):
                                _switch54 = e['whichCan']
                                _switch54_index = -1
                                if _switch54_index < 0 and strict_equal(_switch54, 4): _switch54_index = 0
                                if _switch54_index < 0 and strict_equal(_switch54, 6): _switch54_index = 1
                                if _switch54_index < 0 and strict_equal(_switch54, 7): _switch54_index = 2
                                if _switch54_index < 0 and strict_equal(_switch54, 3): _switch54_index = 3
                                if _switch54_index < 0 and strict_equal(_switch54, 5): _switch54_index = 4
                                if _switch54_index < 0: _switch54_index = -1
                                while True:
                                    if 0 <= _switch54_index <= 0:
                                        if truth(binary('<', call(get(e['rng'], 'NextDouble')), binary('+', 0.2, get(e['save'], 'dailyLuck')))):
                                            _switch55 = call(get(e['rng'], 'Next'), 3)
                                            _switch55_index = -1
                                            if _switch55_index < 0 and strict_equal(_switch55, 0): _switch55_index = 0
                                            if _switch55_index < 0 and strict_equal(_switch55, 1): _switch55_index = 1
                                            if _switch55_index < 0 and strict_equal(_switch55, 2): _switch55_index = 2
                                            if _switch55_index < 0: _switch55_index = -1
                                            while True:
                                                if 0 <= _switch55_index <= 0:
                                                    e.set('trashItem', call(e['wikify'], 'Copper Ore'))
                                                    break
                                                if 0 <= _switch55_index <= 1:
                                                    e.set('trashItem', call(e['wikify'], 'Iron Ore'))
                                                    break
                                                if 0 <= _switch55_index <= 2:
                                                    e.set('trashItem', call(e['wikify'], 'Coal'))
                                                    break
                                                break
                                            e.set('stack', call(get(e['rng'], 'Next'), 1, 5))
                                            if truth(binary('>', e['stack'], 1)):
                                                e.set('trashItem', binary('+', e['trashItem'], binary('+', ' x', e['stack'])))
                                        break
                                    if 0 <= _switch54_index <= 1:
                                        if truth(binary('<', call(get(e['rng'], 'NextDouble')), binary('+', 0.2, get(e['save'], 'dailyLuck')))):
                                            e.set('trashItem', call(e['wikify'], 'Cookie'))
                                        break
                                    if 0 <= _switch54_index <= 2:
                                        e.set('rngSynced', call(e['CSRandom'], call(e['getRandomSeed'], call(e['getHashFromString'], 'garbage_joja'), get(e['save'], 'gameID'), binary('+', e['day'], get(e['save'], 'dayAdjust')))))
                                        if truth(binary('<', call(get(e['rngSynced'], 'NextDouble')), 0.2)):
                                            if truth(get(e['save'], 'theaterUnlocked')):
                                                if truth(binary('>', call(get(e['rng'], 'Next'), 4), 0)):
                                                    e.set('trashItem', call(e['wikify'], 'Corn'))
                                                else:
                                                    e.set('trashItem', call(e['wikify'], 'Movie Ticket'))
                                            else:
                                                if truth(unary('!', get(e['save'], 'ccComplete'))):
                                                    e.set('trashItem', call(e['wikify'], 'Joja Cola'))
                                        break
                                    if 0 <= _switch54_index <= 3:
                                        e.set('rngSynced', call(e['CSRandom'], call(e['getRandomSeed'], call(e['getHashFromString'], 'garbage_museum_535'), get(e['save'], 'gameID'), binary('+', e['day'], get(e['save'], 'dayAdjust')))))
                                        if truth(binary('<', call(get(e['rngSynced'], 'NextDouble')), binary('+', 0.2, get(e['save'], 'dailyLuck')))):
                                            e.set('rngSynced', call(e['CSRandom'], call(e['getRandomSeed'], call(e['getHashFromString'], 'garbage_museum_749'), get(e['save'], 'gameID'), binary('+', e['day'], get(e['save'], 'dayAdjust')))))
                                            if truth(binary('<', call(get(e['rngSynced'], 'NextDouble')), 0.05)):
                                                e.set('trashItem', call(e['wikify'], 'Omni Geode'))
                                            else:
                                                e.set('trashItem', call(e['wikify'], 'Geode'))
                                        break
                                    if 0 <= _switch54_index <= 4:
                                        e.set('rngSynced', call(e['CSRandom'], call(e['getRandomSeed'], call(e['getHashFromString'], 'garbage_saloon_dish'), get(e['save'], 'gameID'), binary('+', e['day'], get(e['save'], 'dayAdjust')))))
                                        if truth(binary('<', call(get(e['rngSynced'], 'NextDouble')), binary('+', 0.2, get(e['save'], 'dailyLuck')))):
                                            e.set('trashItem', '<a href="https://stardewvalleywiki.com/The_Stardrop_Saloon#Rotating_Stock">Dish of the Day</a>')
                                        break
                                    break
                    if truth(binary('===', e['trashItem'], '')):
                        e.set('mega', (binary('<', call(get(e['rng'], 'NextDouble')), 0.01) if truth(_logic56 := binary('>=', get(get(e['save'], 'trashCansChecked'), 0), 20)) else _logic56))
                        if truth((_logic57 if truth(_logic57 := e['mega']) else e['baseChancePassed'])):
                            e.set('roll', call(get(e['rng'], 'Next'), (7 if truth(e['mega']) else get(e['fallbackList'], 'length'))))
                            if truth(binary('===', get(e['fallbackList'], e['roll']), 'SEASON')):
                                e.set('trashItem', call(e['wikify'], call(e['getRandomItemFromSeason'], e['rng'], binary('%', e['month'], 4))))
                            else:
                                e.set('trashItem', call(e['wikify'], get(get(get(e['save'], 'objects'), get(e['fallbackList'], e['roll'])), 'name')))
                else:
                    e.set('mega', (True if truth(binary('<', call(get(e['rng'], 'NextDouble')), 0.01)) else False))
                    e.set('doubleMega', (True if truth((binary('<', call(get(e['rng'], 'NextDouble')), 0.002) if truth(_logic58 := binary('>=', get(get(e['save'], 'trashCansChecked'), 0), 20)) else _logic58)) else False))
                    if truth(e['doubleMega']):
                        e.set('trashItem', call(e['wikify'], 'Garbage Hat'))
                    else:
                        if truth((_logic59 if truth(_logic59 := e['mega']) else binary('<', call(get(e['rng'], 'NextDouble')), e['luckCheck']))):
                            _switch60 = call(get(e['rng'], 'Next'), 10)
                            _switch60_index = -1
                            if _switch60_index < 0 and strict_equal(_switch60, 0): _switch60_index = 0
                            if _switch60_index < 0 and strict_equal(_switch60, 1): _switch60_index = 1
                            if _switch60_index < 0 and strict_equal(_switch60, 2): _switch60_index = 2
                            if _switch60_index < 0 and strict_equal(_switch60, 3): _switch60_index = 3
                            if _switch60_index < 0 and strict_equal(_switch60, 4): _switch60_index = 4
                            if _switch60_index < 0 and strict_equal(_switch60, 5): _switch60_index = 5
                            if _switch60_index < 0 and strict_equal(_switch60, 6): _switch60_index = 6
                            if _switch60_index < 0 and strict_equal(_switch60, 7): _switch60_index = 7
                            if _switch60_index < 0 and strict_equal(_switch60, 8): _switch60_index = 8
                            if _switch60_index < 0 and strict_equal(_switch60, 9): _switch60_index = 9
                            if _switch60_index < 0: _switch60_index = -1
                            while True:
                                if 0 <= _switch60_index <= 0:
                                    e.set('trashItem', call(e['wikify'], 'Trash (item)'))
                                    break
                                if 0 <= _switch60_index <= 1:
                                    e.set('trashItem', call(e['wikify'], 'Joja Cola'))
                                    break
                                if 0 <= _switch60_index <= 2:
                                    e.set('trashItem', call(e['wikify'], 'Broken Glasses'))
                                    break
                                if 0 <= _switch60_index <= 3:
                                    e.set('trashItem', call(e['wikify'], 'Broken CD'))
                                    break
                                if 0 <= _switch60_index <= 4:
                                    e.set('trashItem', call(e['wikify'], 'Soggy Newspaper'))
                                    break
                                if 0 <= _switch60_index <= 5:
                                    e.set('trashItem', call(e['wikify'], 'Bread'))
                                    break
                                if 0 <= _switch60_index <= 6:
                                    e.set('rngSeason', call(e['CSRandom'], binary('+', binary('+', binary('+', binary('+', get(e['save'], 'gameID'), e['day']), get(e['save'], 'dayAdjust')), binary('*', get(e['tileX'], e['whichCan']), 653)), binary('*', get(e['tileY'], e['whichCan']), 777))))
                                    e.set('trashItem', call(e['wikify'], call(e['getRandomItemFromSeason'], e['rngSeason'], binary('%', e['month'], 4))))
                                    break
                                if 0 <= _switch60_index <= 7:
                                    e.set('trashItem', call(e['wikify'], 'Field Snack'))
                                    break
                                if 0 <= _switch60_index <= 8:
                                    _switch61 = call(get(e['rng'], 'Next'), 3)
                                    _switch61_index = -1
                                    if _switch61_index < 0 and strict_equal(_switch61, 0): _switch61_index = 0
                                    if _switch61_index < 0 and strict_equal(_switch61, 1): _switch61_index = 1
                                    if _switch61_index < 0 and strict_equal(_switch61, 2): _switch61_index = 2
                                    if _switch61_index < 0: _switch61_index = -1
                                    while True:
                                        if 0 <= _switch61_index <= 0:
                                            e.set('trashItem', call(e['wikify'], 'Acorn'))
                                            break
                                        if 0 <= _switch61_index <= 1:
                                            e.set('trashItem', call(e['wikify'], 'Maple Seed'))
                                            break
                                        if 0 <= _switch61_index <= 2:
                                            e.set('trashItem', call(e['wikify'], 'Pine Cone'))
                                            break
                                        break
                                    break
                                if 0 <= _switch60_index <= 9:
                                    e.set('trashItem', call(e['wikify'], 'Green Algae'))
                                    break
                                break
                            if truth((binary('<', call(get(e['rng'], 'NextDouble')), e['luckCheck']) if truth(_logic62 := binary('===', e['whichCan'], 3)) else _logic62)):
                                e.set('trashItem', call(e['wikify'], 'Geode'))
                                if truth(binary('<', call(get(e['rng'], 'NextDouble')), 0.05)):
                                    e.set('trashItem', call(e['wikify'], 'Omni Geode'))
                            if truth((binary('<', call(get(e['rng'], 'NextDouble')), e['luckCheck']) if truth(_logic63 := binary('===', e['whichCan'], 4)) else _logic63)):
                                _switch64 = call(get(e['rng'], 'Next'), 3)
                                _switch64_index = -1
                                if _switch64_index < 0 and strict_equal(_switch64, 0): _switch64_index = 0
                                if _switch64_index < 0 and strict_equal(_switch64, 1): _switch64_index = 1
                                if _switch64_index < 0 and strict_equal(_switch64, 2): _switch64_index = 2
                                if _switch64_index < 0: _switch64_index = -1
                                while True:
                                    if 0 <= _switch64_index <= 0:
                                        e.set('trashItem', call(e['wikify'], 'Copper Ore'))
                                        break
                                    if 0 <= _switch64_index <= 1:
                                        e.set('trashItem', call(e['wikify'], 'Iron Ore'))
                                        break
                                    if 0 <= _switch64_index <= 2:
                                        e.set('trashItem', call(e['wikify'], 'Coal'))
                                        break
                                    break
                                call(get(e['rng'], 'Next'), 1, 5)
                            if truth((binary('<', call(get(e['rng'], 'NextDouble')), e['luckCheck']) if truth(_logic65 := binary('===', e['whichCan'], 5)) else _logic65)):
                                e.set('trashItem', '<a href="https://stardewvalleywiki.com/The_Stardrop_Saloon#Rotating_Stock">Dish of the Day</a>')
                            if truth((binary('<', call(get(e['rng'], 'NextDouble')), e['luckCheck']) if truth(_logic66 := binary('===', e['whichCan'], 6)) else _logic66)):
                                e.set('trashItem', call(e['wikify'], 'Cookie'))
                            if truth((binary('<', call(get(e['rng'], 'NextDouble')), 0.2) if truth(_logic67 := binary('===', e['whichCan'], 7)) else _logic67)):
                                e.set('trashItem', call(e['wikify'], 'Joja Cola'))
                                if truth(binary('<', call(get(e['rng'], 'NextDouble')), 0.25)):
                                    e.set('trashItem', binary('+', e['trashItem'], binary('+', ' or ', call(e['wikify'], 'Movie Ticket'))))
                                else:
                                    e.set('trashItem', binary('+', e['trashItem'], binary('+', ' or ', call(e['wikify'], 'Corn'))))
                if truth(binary('!==', e['trashItem'], '')):
                    e.set('trashText', binary('+', binary('+', binary('+', '<em>', get(e['canList'], e['whichCan'])), ':</em> '), e['trashItem']))
                    if truth(e['doubleMega']):
                        e.set('trashText', binary('+', binary('+', '<span class="strong">', e['trashText']), '</span>'))
                    call(get(e['goodStuff'], 'push'), e['trashText'])
                update_env(e, 'whichCan', 1, False)
            if truth(binary('<', e['day'], get(e['save'], 'daysPlayed'))):
                e.set('tclass', 'past')
            else:
                if truth(binary('===', e['day'], get(e['save'], 'daysPlayed'))):
                    e.set('tclass', 'current')
                else:
                    e.set('tclass', 'future')
            e.set('results', '')
            if truth(binary('===', get(e['goodStuff'], 'length'), 0)):
                e.set('results', '<span class="none">None</span>')
            else:
                e.set('results', call(get(call(get(e['goodStuff'], 'sort')), 'join'), ',<br/>'))
            e.set('output', binary('+', e['output'], binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', '<td class="compact ', e['tclass']), '"><span class="date"> '), binary('-', e['day'], e['offset'])), '</span><br/>'), '<span class="cell">'), e['results']), '</span></td>')))
            update_env(e, 'weekDay', 1, False)
        e.set('output', binary('+', e['output'], '</tr>\n'))
        update_env(e, 'week', 1, False)
    e.set('output', binary('+', e['output'], '</tbody></table>\n'))
    return e['output']
    return U


def predictWallpaper_68(parent, this, args):
    # Upstream predictor: 4518
    e = Env(parent)
    e.declare(['day', 'eq_j', 'eq_p', 'fl_j', 'fl_p', 'month', 'monthName', 'output', 'rng_j', 'rng_p', 'showJoja', 'showPierre', 'tclass', 'week', 'weekDay', 'wp_j', 'wp_p', 'year'])
    e.local['arguments'] = Array(args)
    e.local['isSearch'] = (args[0] if len(args) > 0 and args[0] is not U else U)
    e.local['offset'] = (args[1] if len(args) > 1 and args[1] is not U else U)
    e.set('output', '')
    if truth(binary('===', unary('typeof', e['offset']), 'undefined')):
        e.set('offset', binary('*', 7, call(get(e['Math'], 'floor'), binary('/', binary('-', get(e['save'], 'daysPlayed'), 1), 7))))
    if truth(binary('<', e['offset'], 112)):
        call(get(call(e['$'], '#wallpaper-prev-year'), 'prop'), 'disabled', True)
    else:
        call(get(call(e['$'], '#wallpaper-prev-year'), 'val'), binary('-', e['offset'], 112))
        call(get(call(e['$'], '#wallpaper-prev-year'), 'prop'), 'disabled', False)
    if truth(binary('<', e['offset'], 7)):
        call(get(call(e['$'], '#wallpaper-prev-week'), 'prop'), 'disabled', True)
    else:
        call(get(call(e['$'], '#wallpaper-prev-week'), 'val'), binary('-', e['offset'], 7))
        call(get(call(e['$'], '#wallpaper-prev-week'), 'prop'), 'disabled', False)
    call(get(call(e['$'], '#wallpaper-reset'), 'val'), 'reset')
    call(get(call(e['$'], '#wallpaper-next-week'), 'val'), binary('+', e['offset'], 7))
    call(get(call(e['$'], '#wallpaper-next-year'), 'val'), binary('+', e['offset'], 112))
    e.set('month', call(get(e['Math'], 'floor'), binary('/', e['offset'], 28)))
    e.set('monthName', get(get(e['save'], 'seasonNames'), binary('%', e['month'], 4)))
    e.set('year', binary('+', 1, call(get(e['Math'], 'floor'), binary('/', e['offset'], 112))))
    e.set('output', binary('+', e['output'], binary('+', binary('+', '<table class="output"><thead><tr><th class="day">Date</th>', '<th class="wp-result"><img src="blank.png" class="dark icon" id="pierre"> Pierre\'s General Store</th>'), '<th class="wp-result"><img src="blank.png" class="dark icon" id="morris"> Joja Mart</th></tr></thead><tbody>')))
    e.set('weekDay', 1)
    while truth(binary('<', e['weekDay'], 8)):
        e.set('day', binary('+', e['weekDay'], e['offset']))
        if truth(binary('>=', call(e['compareSemVer'], get(e['save'], 'version'), '1.6'), 0)):
            e.set('rng_p', call(e['CSRandom'], call(e['getRandomSeed'], binary('+', e['day'], get(e['save'], 'dayAdjust')), binary('/', get(e['save'], 'gameID'), 2))))
            e.set('rng_j', call(e['CSRandom'], call(e['getRandomSeed'], binary('+', e['day'], get(e['save'], 'dayAdjust')), binary('/', get(e['save'], 'gameID'), 2))))
            e.set('wp_p', get(call(e['getRandomWallFloor'], e['rng_p'], 0, 111, 9, Obj({'21': True})), 0))
            e.set('fl_p', binary('+', 1, get(call(e['getRandomWallFloor'], e['rng_p'], 0, 55, 22), 0)))
            e.set('wp_j', get(call(e['getRandomWallFloor'], e['rng_j'], 0, 111, 9, Obj({'21': True})), 0))
            e.set('fl_j', binary('+', 1, get(call(e['getRandomWallFloor'], e['rng_j'], 0, 39, 48), 0)))
        else:
            e.set('rng_p', call(e['CSRandom'], binary('+', binary('+', e['day'], binary('/', get(e['save'], 'gameID'), 2)), get(e['save'], 'dayAdjust'))))
            e.set('rng_j', call(e['CSRandom'], binary('+', binary('+', binary('+', e['day'], binary('/', get(e['save'], 'gameID'), 2)), 1), get(e['save'], 'dayAdjust'))))
            e.set('wp_p', call(get(e['rng_p'], 'Next'), 112))
            e.set('fl_p', binary('+', 1, call(get(e['rng_p'], 'Next'), 40)))
            e.set('wp_j', call(get(e['rng_j'], 'Next'), 112))
            if truth(binary('===', e['wp_j'], 21)):
                e.set('wp_j', 22)
            e.set('fl_j', binary('+', 1, call(get(e['rng_j'], 'Next'), 40)))
        if truth(call(get(get(e['save'], 'wallpaperEquiv'), 'hasOwnProperty'), e['wp_p'])):
            e.set('eq_p', call(e['wikify'], get(get(e['save'], 'wallpaperEquiv'), e['wp_p'])))
        else:
            e.set('eq_p', '(No valid equivalence)')
        update_env(e, 'wp_p', 1, False)
        if truth(call(get(get(e['save'], 'wallpaperEquiv'), 'hasOwnProperty'), e['wp_j'])):
            e.set('eq_j', call(e['wikify'], get(get(e['save'], 'wallpaperEquiv'), e['wp_j'])))
        else:
            e.set('eq_j', '(No valid equivalence)')
        update_env(e, 'wp_j', 1, False)
        if truth(binary('<', e['day'], get(e['save'], 'daysPlayed'))):
            e.set('tclass', 'past')
        else:
            if truth(binary('===', e['day'], get(e['save'], 'daysPlayed'))):
                e.set('tclass', 'current')
            else:
                e.set('tclass', 'future')
        e.set('showPierre', (_logic69 if truth(_logic69 := get(e['save'], 'ccComplete')) else binary('!==', e['weekDay'], 3)))
        e.set('showJoja', unary('!', get(e['save'], 'ccComplete')))
        e.set('output', binary('+', e['output'], binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', '<tr><td class="', e['tclass']), '">'), get(get(e['save'], 'dayNames'), binary('%', binary('-', e['day'], 1), 7))), '<br/>'), e['monthName']), ' '), binary('+', binary('%', binary('-', e['day'], 1), 28), 1)), ', Year '), e['year']), '</td><td class="'), e['tclass']), '">')))
        e.set('output', binary('+', e['output'], (binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', '<div class="wp"><img src="blank.png" class="wp left" id="wp_', e['wp_p']), '"><img src="blank.png" class="wp right" id="wp_'), e['wp_p']), '"> '), 'Wallpaper #'), e['wp_p']), '<br/>'), e['eq_p']), '<br/></div><br/>'), '<div class="fl"><img src="blank.png" class="fl" id="fl_'), e['fl_p']), '"> '), 'Floor # '), e['fl_p']), '</div>') if truth(e['showPierre']) else '(Closed)')))
        e.set('output', binary('+', e['output'], binary('+', binary('+', '</td><td class="', e['tclass']), '">')))
        e.set('output', binary('+', e['output'], (binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', '<div class="wp"><img src="blank.png" class="wp left" id="wp_', e['wp_j']), '"><img src="blank.png" class="wp right" id="wp_'), e['wp_j']), '"> '), 'Wallpaper #'), e['wp_j']), '<br/>'), e['eq_j']), '<br/></div><br/>'), '<div class="fl"><img src="blank.png" class="fl" id="fl_'), e['fl_j']), '"> '), 'Floor # '), e['fl_j']), '</div>') if truth(e['showJoja']) else '(Closed)')))
        e.set('output', binary('+', e['output'], '</td></tr>'))
        update_env(e, 'weekDay', 1, False)
    e.set('output', binary('+', e['output'], '</tbody></table>\n'))
    return e['output']
    return U


def getCartItem_70(parent, this, args):
    # Upstream predictor: 4623
    e = Env(parent)
    e.declare(['failsafe', 'itemID', 'keepGoing', 'theItem'])
    e.local['arguments'] = Array(args)
    e.local['rng'] = (args[0] if len(args) > 0 and args[0] is not U else U)
    e.local['seenItems'] = (args[1] if len(args) > 1 and args[1] is not U else U)
    e.set('theItem', Obj({}))
    e.set('itemID', call(get(e['rng'], 'Next'), 2, 790))
    if truth(binary('>=', call(e['compareSemVer'], get(e['save'], 'version'), '1.4'), 0)):
        e.set('keepGoing', True)
        while truth(e['keepGoing']):
            update_env(e, 'itemID', 1, False)
            e.set('itemID', binary('%', e['itemID'], 790))
            if truth(call(get(get(e['save'], 'cartItems_1_4'), 'hasOwnProperty'), e['itemID'])):
                put(e['theItem'], 'name', get(get(e['save'], 'cartItems_1_4'), e['itemID']))
                put(e['theItem'], 'price', call(get(e['Math'], 'max'), binary('*', call(get(e['rng'], 'Next'), 1, 11), 100), binary('*', get(get(get(e['save'], 'objects'), binary('+', '_', e['itemID'])), 'price'), call(get(e['rng'], 'Next'), 3, 6))))
                put(e['theItem'], 'qty', (5 if truth(binary('<', call(get(e['rng'], 'NextDouble')), 0.1)) else 1))
                if truth(unary('!', binary('in', get(e['theItem'], 'name'), e['seenItems']))):
                    put(e['seenItems'], get(e['theItem'], 'name'), 1)
                    e.set('keepGoing', False)
    else:
        put(e['theItem'], 'name', get(get(e['save'], 'cartItems'), e['itemID']))
        e.set('failsafe', 0)
        while truth(((_logic72 if truth(_logic72 := unary('!', call(get(get(e['save'], 'objects'), 'hasOwnProperty'), binary('+', '_', e['itemID'])))) else binary('!==', get(get(get(e['save'], 'objects'), binary('+', '_', e['itemID'])), 'name'), get(e['theItem'], 'name'))) if truth(_logic71 := binary('<', update_env(e, 'failsafe', 1, False), 800)) else _logic71)):
            update_env(e, 'itemID', 1, False)
            e.set('itemID', binary('%', e['itemID'], 790))
        put(e['theItem'], 'price', call(get(e['Math'], 'max'), binary('*', call(get(e['rng'], 'Next'), 1, 11), 100), binary('*', get(get(get(e['save'], 'objects'), binary('+', '_', e['itemID'])), 'price'), call(get(e['rng'], 'Next'), 3, 6))))
        put(e['theItem'], 'qty', (5 if truth(binary('<', call(get(e['rng'], 'NextDouble')), 0.1)) else 1))
    return e['theItem']
    return U


def predictCart_73(parent, this, args):
    # Upstream predictor: 4664
    e = Env(parent)
    e.declare(['count', 'dayOfMonth', 'dayOfWeek', 'days', 'i', 'isNightMarket', 'item', 'month', 'monthName', 'output', 'price', 'qty', 'rngFirst', 'rngLast', 'rngMid', 'searchEnd', 'searchStart', 'searchTerm', 'seenItems', 'seenItemsFirst', 'seenItemsLast', 'seenItemsMid', 'slot', 'startDay', 'year'])
    e.local['arguments'] = Array(args)
    e.local['isSearch'] = (args[0] if len(args) > 0 and args[0] is not U else U)
    e.local['offset'] = (args[1] if len(args) > 1 and args[1] is not U else U)
    e.set('output', '')
    e.set('isNightMarket', False)
    if truth(binary('>=', call(e['compareSemVer'], get(e['save'], 'version'), '1.6'), 0)):
        return call(e['predictCart_1_6'], e['isSearch'], e['offset'])
    if truth((binary('!==', e['offset'], '') if truth(_logic74 := (binary('!==', unary('typeof', e['offset']), 'undefined') if truth(_logic75 := e['isSearch']) else _logic75)) else _logic74)):
        call(get(call(e['$'], '#cart-prev-year'), 'prop'), 'disabled', True)
        call(get(call(e['$'], '#cart-prev-week'), 'prop'), 'disabled', True)
        call(get(call(e['$'], '#cart-next-week'), 'prop'), 'disabled', True)
        call(get(call(e['$'], '#cart-next-year'), 'prop'), 'disabled', True)
        call(get(call(e['$'], '#cart-reset'), 'html'), 'Clear Search Results &amp; Reset Browsing')
        e.set('searchTerm', call(e['RegExp'], e['offset'], 'i'))
        e.set('searchStart', (0 if truth(call(get(call(e['$'], '#cart-search-all'), 'prop'), 'checked')) else binary('*', 7, call(get(e['Math'], 'floor'), binary('/', binary('-', get(e['save'], 'daysPlayed'), 1), 7)))))
        e.set('searchEnd', binary('*', 112, call(get(call(e['$'], '#cart-search-range'), 'val'))))
        e.set('output', binary('+', e['output'], binary('+', binary('+', binary('+', binary('+', binary('+', '<table class="output"><thead><tr><th colspan="4">Search results for &quot;', e['offset']), '&quot; over the '), ('first ' if truth(call(get(call(e['$'], '#cart-search-all'), 'prop'), 'checked')) else 'next ')), call(get(call(e['$'], '#cart-search-range'), 'val'))), ' year(s)</th></tr>\n')))
        e.set('output', binary('+', e['output'], '<tr><th class="day">Day</th><th class="item">Item</th><th class="qty">Qty</th><th class="price">Price</th></tr>\n<tbody>'))
        e.set('count', 0)
        e.set('offset', e['searchStart'])
        while truth(binary('<', e['offset'], binary('+', e['searchStart'], e['searchEnd']))):
            e.set('days', Array([5, 7]))
            if truth((binary('===', binary('%', e['offset'], 112), 98) if truth(_logic76 := binary('>=', call(e['compareSemVer'], get(e['save'], 'version'), '1.3'), 0)) else _logic76)):
                e.set('days', Array([1, 2, 3, 5, 7]))
            e.set('month', call(get(e['Math'], 'floor'), binary('/', e['offset'], 28)))
            e.set('monthName', get(get(e['save'], 'seasonNames'), binary('%', e['month'], 4)))
            e.set('year', binary('+', 1, call(get(e['Math'], 'floor'), binary('/', e['offset'], 112))))
            e.set('i', 0)
            while truth(binary('<', e['i'], get(e['days'], 'length'))):
                e.set('seenItems', Obj({}))
                e.set('dayOfMonth', binary('+', binary('%', e['offset'], 28), get(e['days'], e['i'])))
                e.set('dayOfWeek', get(get(e['save'], 'dayNames'), binary('-', get(e['days'], e['i']), 1)))
                e.set('rngFirst', call(e['CSRandom'], binary('+', binary('+', binary('+', get(e['save'], 'gameID'), e['offset']), get(e['days'], e['i'])), get(e['save'], 'dayAdjust'))))
                e.set('slot', 1)
                while truth(binary('<=', e['slot'], 10)):
                    e.set('item', call(e['getCartItem'], e['rngFirst'], e['seenItems']))
                    if truth(call(get(e['searchTerm'], 'test'), get(e['item'], 'name'))):
                        update_env(e, 'count', 1, False)
                        e.set('output', binary('+', e['output'], binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', '<tr><td>', e['dayOfWeek']), ' '), e['monthName']), ' '), e['dayOfMonth']), ', Year '), e['year']), '</td><td>'), call(e['wikify'], get(e['item'], 'name'))), '</td><td>'), get(e['item'], 'qty')), '</td><td>'), call(e['addCommas'], get(e['item'], 'price'))), 'g</td>')))
                    update_env(e, 'slot', 1, False)
                e.set('slot', unary('-', 1))
                while truth(unary('!', call(get(get(e['save'], 'cartFurniture'), 'hasOwnProperty'), e['slot']))):
                    e.set('slot', call(get(e['rngFirst'], 'Next'), 0, 1613))
                e.set('item', get(get(e['save'], 'cartFurniture'), e['slot']))
                e.set('price', binary('*', call(get(e['rngFirst'], 'Next'), 1, 11), 250))
                if truth(call(get(e['searchTerm'], 'test'), e['item'])):
                    update_env(e, 'count', 1, False)
                    e.set('output', binary('+', e['output'], binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', '<tr><td>', e['dayOfWeek']), ' '), e['monthName']), ' '), e['dayOfMonth']), ', Year '), e['year']), '</td><td>'), call(e['wikify'], e['item'], 'Furniture')), '</td><td>'), e['qty']), '</td><td>'), call(e['addCommas'], e['price'])), 'g</td>')))
                if truth(binary('<', binary('%', e['month'], 4), 2)):
                    e.set('item', 'Rare Seed')
                    e.set('price', 1000)
                    e.set('qty', (5 if truth(binary('<', call(get(e['rngFirst'], 'NextDouble')), 0.1)) else 1))
                else:
                    if truth(binary('<', call(get(e['rngFirst'], 'NextDouble')), 0.4)):
                        e.set('item', 'Rarecrow (Snowman)')
                        e.set('qty', 1)
                        e.set('price', '4000g')
                    else:
                        e.set('item', '')
                if truth(call(get(e['searchTerm'], 'test'), e['item'])):
                    update_env(e, 'count', 1, False)
                    e.set('output', binary('+', e['output'], binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', '<tr><td>', e['dayOfWeek']), ' '), e['monthName']), ' '), e['dayOfMonth']), ', Year '), e['year']), '</td><td>'), call(e['wikify'], e['item'])), '</td><td>'), e['qty']), '</td><td>'), call(e['addCommas'], e['price'])), 'g</td>')))
                if truth(binary('<', call(get(e['rngFirst'], 'NextDouble')), 0.25)):
                    e.set('item', 'Coffee Bean')
                    e.set('qty', 1)
                    e.set('price', '2500g')
                else:
                    e.set('item', '')
                if truth(call(get(e['searchTerm'], 'test'), e['item'])):
                    update_env(e, 'count', 1, False)
                    e.set('output', binary('+', e['output'], binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', '<tr><td>', e['dayOfWeek']), ' '), e['monthName']), ' '), e['dayOfMonth']), ', Year '), e['year']), '</td><td>'), call(e['wikify'], e['item'])), '</td><td>'), e['qty']), '</td><td>'), e['price']), 'g</td>')))
                update_env(e, 'i', 1, False)
            e.set('offset', binary('+', e['offset'], 7))
        e.set('output', binary('+', e['output'], binary('+', binary('+', '<tr><td colspan="4" class="count">Found ', e['count']), ' matching item(s)</td></tr></tbody></table>\n')))
    else:
        if truth((_logic77 if truth(_logic77 := binary('===', unary('typeof', e['offset']), 'undefined')) else binary('===', e['offset'], ''))):
            e.set('offset', binary('*', 7, call(get(e['Math'], 'floor'), binary('/', binary('-', get(e['save'], 'daysPlayed'), 1), 7))))
        if truth((binary('===', binary('%', e['offset'], 112), 94) if truth(_logic78 := binary('>=', call(e['compareSemVer'], get(e['save'], 'version'), '1.3'), 0)) else _logic78)):
            e.set('isNightMarket', True)
            call(get(call(e['$'], '#cart-next-week'), 'val'), binary('+', e['offset'], 4))
            call(get(call(e['$'], '#cart-prev-week'), 'val'), binary('-', e['offset'], 3))
            e.set('startDay', 0)
        else:
            e.set('isNightMarket', False)
            e.set('startDay', 4)
            if truth((binary('===', binary('%', e['offset'], 112), 91) if truth(_logic79 := binary('>=', call(e['compareSemVer'], get(e['save'], 'version'), '1.3'), 0)) else _logic79)):
                call(get(call(e['$'], '#cart-next-week'), 'val'), binary('+', e['offset'], 3))
                call(get(call(e['$'], '#cart-prev-week'), 'val'), binary('-', e['offset'], 7))
            else:
                if truth((binary('===', binary('%', e['offset'], 112), 98) if truth(_logic80 := binary('>=', call(e['compareSemVer'], get(e['save'], 'version'), '1.3'), 0)) else _logic80)):
                    call(get(call(e['$'], '#cart-next-week'), 'val'), binary('+', e['offset'], 7))
                    call(get(call(e['$'], '#cart-prev-week'), 'val'), binary('-', e['offset'], 4))
                else:
                    call(get(call(e['$'], '#cart-next-week'), 'val'), binary('+', e['offset'], 7))
                    call(get(call(e['$'], '#cart-prev-week'), 'val'), binary('-', e['offset'], 7))
        call(get(call(e['$'], '#cart-next-year'), 'val'), binary('+', e['offset'], 112))
        call(get(call(e['$'], '#cart-prev-year'), 'val'), binary('-', e['offset'], 112))
        if truth(binary('<', e['offset'], 7)):
            call(get(call(e['$'], '#cart-prev-week'), 'prop'), 'disabled', True)
        else:
            call(get(call(e['$'], '#cart-prev-week'), 'prop'), 'disabled', False)
        if truth(binary('<', e['offset'], 112)):
            call(get(call(e['$'], '#cart-prev-year'), 'prop'), 'disabled', True)
        else:
            call(get(call(e['$'], '#cart-prev-year'), 'prop'), 'disabled', False)
        call(get(call(e['$'], '#cart-reset'), 'val'), 'reset')
        call(get(call(e['$'], '#cart-reset'), 'html'), 'Reset Browsing')
        call(get(call(e['$'], '#cart-next-week'), 'prop'), 'disabled', False)
        call(get(call(e['$'], '#cart-next-year'), 'prop'), 'disabled', False)
        call(get(call(e['$'], '#cart-search-text'), 'val'), '')
        call(get(call(e['$'], '#cart-search-range'), 'val'), 2)
        call(get(call(e['$'], '#cart-search-all'), 'prop'), 'checked', False)
        e.set('month', call(get(e['Math'], 'floor'), binary('/', e['offset'], 28)))
        e.set('monthName', get(get(e['save'], 'seasonNames'), binary('%', e['month'], 4)))
        e.set('year', binary('+', 1, call(get(e['Math'], 'floor'), binary('/', e['offset'], 112))))
        e.set('dayOfMonth', binary('%', e['offset'], 28))
        e.set('output', binary('+', e['output'], binary('+', binary('+', '<table class="output"><thead><tr><th rowspan="2">', ('Night Market<br/>Boat' if truth(e['isNightMarket']) else 'Forest Cart')), '</th>')))
        e.set('output', binary('+', e['output'], binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', '<th colspan="3" class="multi">', get(get(e['save'], 'dayNames'), e['startDay'])), ' '), e['monthName']), ' '), binary('+', e['dayOfMonth'], 5)), ', Year '), e['year']), '</th>')))
        if truth(e['isNightMarket']):
            e.set('output', binary('+', e['output'], binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', '<th colspan="3" class="multi">', get(get(e['save'], 'dayNames'), binary('+', e['startDay'], 1))), ' '), e['monthName']), ' '), binary('+', e['dayOfMonth'], 6)), ', Year '), e['year']), '</th>\n')))
        e.set('output', binary('+', e['output'], binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', '<th colspan="3" class="multi">', get(get(e['save'], 'dayNames'), binary('+', e['startDay'], 2))), ' '), e['monthName']), ' '), binary('+', e['dayOfMonth'], 7)), ', Year '), e['year']), '</th></tr>\n')))
        e.set('output', binary('+', e['output'], '<tr><th class="item">Item</th><th class="qty">Qty</th><th class="price">Price</th>'))
        if truth(e['isNightMarket']):
            e.set('output', binary('+', e['output'], '<th class="item">Item</th><th class="qty">Qty</th><th class="price">Price</th>'))
        e.set('output', binary('+', e['output'], '<th class="item">Item</th><th class="qty">Qty</th><th class="price">Price</th></tr>\n<tbody>'))
        e.set('rngFirst', call(e['CSRandom'], binary('+', binary('+', binary('+', get(e['save'], 'gameID'), e['offset']), 5), get(e['save'], 'dayAdjust'))))
        if truth(e['isNightMarket']):
            e.set('rngMid', call(e['CSRandom'], binary('+', binary('+', binary('+', get(e['save'], 'gameID'), e['offset']), 6), get(e['save'], 'dayAdjust'))))
        e.set('rngLast', call(e['CSRandom'], binary('+', binary('+', binary('+', get(e['save'], 'gameID'), e['offset']), 7), get(e['save'], 'dayAdjust'))))
        e.set('seenItemsFirst', Obj({}))
        e.set('seenItemsMid', Obj({}))
        e.set('seenItemsLast', Obj({}))
        e.set('slot', 1)
        while truth(binary('<=', e['slot'], 10)):
            e.set('output', binary('+', e['output'], binary('+', binary('+', '<tr><td>Basic Item ', e['slot']), '</td>')))
            e.set('item', call(e['getCartItem'], e['rngFirst'], e['seenItemsFirst']))
            e.set('output', binary('+', e['output'], binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', '<td class="item">', call(e['wikify'], get(e['item'], 'name'))), '</td><td>'), get(e['item'], 'qty')), '</td><td>'), call(e['addCommas'], get(e['item'], 'price'))), 'g</td>')))
            if truth(e['isNightMarket']):
                e.set('item', call(e['getCartItem'], e['rngMid'], e['seenItemsMid']))
                e.set('output', binary('+', e['output'], binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', '<td class="item">', call(e['wikify'], get(e['item'], 'name'))), '</td><td>'), get(e['item'], 'qty')), '</td><td>'), call(e['addCommas'], get(e['item'], 'price'))), 'g</td>')))
            e.set('item', call(e['getCartItem'], e['rngLast'], e['seenItemsLast']))
            e.set('output', binary('+', e['output'], binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', '<td class="item">', call(e['wikify'], get(e['item'], 'name'))), '</td><td>'), get(e['item'], 'qty')), '</td><td>'), call(e['addCommas'], get(e['item'], 'price'))), 'g</td></tr>')))
            update_env(e, 'slot', 1, False)
        e.set('slot', unary('-', 1))
        while truth(unary('!', call(get(get(e['save'], 'cartFurniture'), 'hasOwnProperty'), e['slot']))):
            e.set('slot', call(get(e['rngFirst'], 'Next'), 0, 1613))
        e.set('item', get(get(e['save'], 'cartFurniture'), e['slot']))
        e.set('price', binary('*', call(get(e['rngFirst'], 'Next'), 1, 11), 250))
        e.set('output', binary('+', e['output'], binary('+', binary('+', binary('+', binary('+', '<tr><td>Furniture</td><td class="item">', call(e['wikify'], e['item'], 'Furniture')), '</td><td>1</td><td>'), call(e['addCommas'], e['price'])), 'g</td>')))
        if truth(e['isNightMarket']):
            e.set('slot', unary('-', 1))
            while truth(unary('!', call(get(get(e['save'], 'cartFurniture'), 'hasOwnProperty'), e['slot']))):
                e.set('slot', call(get(e['rngMid'], 'Next'), 0, 1613))
            e.set('item', get(get(e['save'], 'cartFurniture'), e['slot']))
            e.set('price', binary('*', call(get(e['rngMid'], 'Next'), 1, 11), 250))
            e.set('output', binary('+', e['output'], binary('+', binary('+', binary('+', binary('+', '<td class="item">', call(e['wikify'], e['item'], 'Furniture')), '</td><td>1</td><td>'), call(e['addCommas'], e['price'])), 'g</td>')))
        e.set('slot', unary('-', 1))
        while truth(unary('!', call(get(get(e['save'], 'cartFurniture'), 'hasOwnProperty'), e['slot']))):
            e.set('slot', call(get(e['rngLast'], 'Next'), 0, 1613))
        e.set('item', get(get(e['save'], 'cartFurniture'), e['slot']))
        e.set('price', binary('*', call(get(e['rngLast'], 'Next'), 1, 11), 250))
        e.set('output', binary('+', e['output'], binary('+', binary('+', binary('+', binary('+', '<td class="item">', call(e['wikify'], e['item'], 'Furniture')), '</td><td>1</td><td>'), call(e['addCommas'], e['price'])), 'g</td></tr>')))
        e.set('output', binary('+', e['output'], '<tr><td>Seasonal Special</td>'))
        if truth(binary('<', binary('%', e['month'], 4), 2)):
            e.set('item', 'Rare Seed')
            e.set('price', 1000)
            e.set('qty', (5 if truth(binary('<', call(get(e['rngFirst'], 'NextDouble')), 0.1)) else 1))
            e.set('output', binary('+', e['output'], binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', '<td class="item">', call(e['wikify'], e['item'])), '</td><td>'), e['qty']), '</td><td>'), call(e['addCommas'], e['price'])), 'g</td>')))
            if truth(e['isNightMarket']):
                e.set('qty', (5 if truth(binary('<', call(get(e['rngMid'], 'NextDouble')), 0.1)) else 1))
                e.set('output', binary('+', e['output'], binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', '<td class="item">', call(e['wikify'], e['item'])), '</td><td>'), e['qty']), '</td><td>'), call(e['addCommas'], e['price'])), 'g</td>')))
            e.set('qty', (5 if truth(binary('<', call(get(e['rngLast'], 'NextDouble')), 0.1)) else 1))
            e.set('output', binary('+', e['output'], binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', '<td class="item">', call(e['wikify'], e['item'])), '</td><td>'), e['qty']), '</td><td>'), call(e['addCommas'], e['price'])), 'g</td></tr>')))
        else:
            if truth(binary('<', call(get(e['rngFirst'], 'NextDouble')), 0.4)):
                e.set('item', call(e['wikify'], 'Rarecrow (Snowman)'))
                e.set('qty', 1)
                e.set('price', '4000g')
            else:
                e.set('item', '(None)')
                e.set('qty', '--')
                e.set('price', '--')
            e.set('output', binary('+', e['output'], binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', '<td class="item">', e['item']), '</td><td>'), e['qty']), '</td><td>'), call(e['addCommas'], e['price'])), '</td>')))
            if truth(e['isNightMarket']):
                if truth(binary('<', call(get(e['rngMid'], 'NextDouble')), 0.4)):
                    e.set('item', call(e['wikify'], 'Rarecrow (Snowman)'))
                    e.set('qty', 1)
                    e.set('price', '4000g')
                else:
                    e.set('item', '(None)')
                    e.set('qty', '--')
                    e.set('price', '--')
                e.set('output', binary('+', e['output'], binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', '<td class="item">', e['item']), '</td><td>'), e['qty']), '</td><td>'), call(e['addCommas'], e['price'])), '</td>')))
            if truth(binary('<', call(get(e['rngLast'], 'NextDouble')), 0.4)):
                e.set('item', call(e['wikify'], 'Rarecrow (Snowman)'))
                e.set('qty', 1)
                e.set('price', '4000g')
            else:
                e.set('item', '(None)')
                e.set('qty', '--')
                e.set('price', '--')
            e.set('output', binary('+', e['output'], binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', '<td class="item">', e['item']), '</td><td>'), e['qty']), '</td><td>'), call(e['addCommas'], e['price'])), '</td></tr>')))
        e.set('output', binary('+', e['output'], '<tr><td>Other Special</td>'))
        if truth(binary('<', call(get(e['rngFirst'], 'NextDouble')), 0.25)):
            e.set('item', call(e['wikify'], 'Coffee Bean'))
            e.set('qty', 1)
            e.set('price', '2500g')
        else:
            e.set('item', '(None)')
            e.set('qty', '--')
            e.set('price', '--')
        e.set('output', binary('+', e['output'], binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', '<td class="item">', e['item']), '</td><td>'), e['qty']), '</td><td>'), call(e['addCommas'], e['price'])), '</td>')))
        if truth(e['isNightMarket']):
            if truth(binary('<', call(get(e['rngMid'], 'NextDouble')), 0.25)):
                e.set('item', call(e['wikify'], 'Coffee Bean'))
                e.set('qty', 1)
                e.set('price', '2500g')
            else:
                e.set('item', '(None)')
                e.set('qty', '--')
                e.set('price', '--')
            e.set('output', binary('+', e['output'], binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', '<td class="item">', e['item']), '</td><td>'), e['qty']), '</td><td>'), call(e['addCommas'], e['price'])), '</td>')))
        if truth(binary('<', call(get(e['rngLast'], 'NextDouble')), 0.25)):
            e.set('item', call(e['wikify'], 'Coffee Bean'))
            e.set('qty', 1)
            e.set('price', '2500g')
        else:
            e.set('item', '(None)')
            e.set('qty', '--')
            e.set('price', '--')
        e.set('output', binary('+', e['output'], binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', '<td class="item">', e['item']), '</td><td>'), e['qty']), '</td><td>'), call(e['addCommas'], e['price'])), '</td></tr>')))
        e.set('output', binary('+', e['output'], '</tbody></table>\n'))
    return e['output']
    return U


def getRandomItems_81(parent, this, args):
    # Upstream predictor: 4970
    e = Env(parent)
    e.declare(['id', 'index', 'key', 'selectedItems', 'shuffledItems', 'slot'])
    e.local['arguments'] = Array(args)
    e.local['rng'] = (args[0] if len(args) > 0 and args[0] is not U else U)
    e.local['type'] = (args[1] if len(args) > 1 and args[1] is not U else U)
    e.local['min'] = (args[2] if len(args) > 2 and args[2] is not U else U)
    e.local['max'] = (args[3] if len(args) > 3 and args[3] is not U else U)
    e.local['requirePrice'] = (args[4] if len(args) > 4 and args[4] is not U else U)
    e.local['isRandomSale'] = (args[5] if len(args) > 5 and args[5] is not U else U)
    e.local['doCategoryChecks'] = (args[6] if len(args) > 6 and args[6] is not U else False)
    e.local['howMany'] = (args[7] if len(args) > 7 and args[7] is not U else 1)
    e.set('shuffledItems', Obj({}))
    for _key82 in keys(get(e['save'], e['type'])):
        e.set('id', _key82)
        e.set('key', call(get(e['rng'], 'Next')))
        if truth(call(e['isNaN'], get(get(get(e['save'], e['type']), e['id']), 'id'))):
            continue
        if truth((binary('==', get(get(get(e['save'], e['type']), e['id']), 'price'), 0) if truth(_logic83 := e['requirePrice']) else _logic83)):
            continue
        if truth((get(get(get(e['save'], e['type']), e['id']), 'offlimits') if truth(_logic84 := e['isRandomSale']) else _logic84)):
            continue
        e.set('index', call(e['parseInt'], get(get(get(e['save'], e['type']), e['id']), 'id')))
        if truth((binary('<=', e['index'], e['max']) if truth(_logic85 := binary('>=', e['index'], e['min'])) else _logic85)):
            put(e['shuffledItems'], e['key'], e['id'])
    e.set('selectedItems', Array([]))
    e.set('slot', 1)
    for _key86 in keys(e['shuffledItems']):
        e.set('key', _key86)
        if truth(((_logic88 if truth(_logic88 := binary('>=', get(get(get(e['save'], e['type']), get(e['shuffledItems'], e['key'])), 'category'), 0)) else binary('===', get(get(get(e['save'], e['type']), get(e['shuffledItems'], e['key'])), 'category'), unary('-', 999))) if truth(_logic87 := e['doCategoryChecks']) else _logic87)):
            continue
        if truth(((_logic90 if truth(_logic90 := (_logic91 if truth(_logic91 := binary('===', get(get(get(e['save'], e['type']), get(e['shuffledItems'], e['key'])), 'type'), 'Arch')) else binary('===', get(get(get(e['save'], e['type']), get(e['shuffledItems'], e['key'])), 'type'), 'Minerals'))) else binary('===', get(get(get(e['save'], e['type']), get(e['shuffledItems'], e['key'])), 'type'), 'Quest')) if truth(_logic89 := e['doCategoryChecks']) else _logic89)):
            continue
        call(get(e['selectedItems'], 'push'), get(e['shuffledItems'], e['key']))
        if truth(binary('>=', update_env(e, 'slot', 1, False), e['howMany'])):
            break
    return e['selectedItems']
    return U


def getRandomWallFloor_92(parent, this, args):
    # Upstream predictor: 5009
    e = Env(parent)
    e.declare(['id', 'key', 'selectedItems', 'shuffledItems', 'slot'])
    e.local['arguments'] = Array(args)
    e.local['rng'] = (args[0] if len(args) > 0 and args[0] is not U else U)
    e.local['min'] = (args[1] if len(args) > 1 and args[1] is not U else U)
    e.local['max'] = (args[2] if len(args) > 2 and args[2] is not U else U)
    e.local['extra'] = (args[3] if len(args) > 3 and args[3] is not U else U)
    e.local['exclude'] = (args[4] if len(args) > 4 and args[4] is not U else Obj({}))
    e.local['howMany'] = (args[5] if len(args) > 5 and args[5] is not U else 1)
    e.set('shuffledItems', Obj({}))
    e.set('id', e['min'])
    while truth(binary('<=', e['id'], binary('+', e['max'], e['extra']))):
        e.set('key', call(get(e['rng'], 'Next')))
        put(e['shuffledItems'], e['key'], e['id'])
        update_env(e, 'id', 1, False)
    e.set('selectedItems', Array([]))
    e.set('slot', 1)
    for _key93 in keys(e['shuffledItems']):
        e.set('key', _key93)
        if truth((_logic94 if truth(_logic94 := call(get(e['exclude'], 'hasOwnProperty'), get(e['shuffledItems'], e['key']))) else binary('>', get(e['shuffledItems'], e['key']), e['max']))):
            continue
        call(get(e['selectedItems'], 'push'), get(e['shuffledItems'], e['key']))
        if truth(binary('>=', update_env(e, 'slot', 1, False), e['howMany'])):
            break
    return e['selectedItems']
    return U


def predictCart_1_6_95(parent, this, args):
    # Upstream predictor: 5033
    e = Env(parent)
    e.declare(['cart', 'cartName', 'count', 'd', 'dayOfMonth', 'dayOfPrediction', 'dayOfWeek', 'dayOfYear', 'days', 'i', 'item', 'month', 'monthName', 'name', 'nameOffset', 'output', 'pick', 'price', 'qty', 'rng', 'rngSynced', 'searchEnd', 'searchStart', 'searchTerm', 'seenRareSeed', 'skillBookList', 'slot', 'span', 'startDay', 'visitsNow', 'year'])
    e.local['arguments'] = Array(args)
    e.local['isSearch'] = (args[0] if len(args) > 0 and args[0] is not U else U)
    e.local['offset'] = (args[1] if len(args) > 1 and args[1] is not U else U)
    e.set('output', '')
    e.set('skillBookList', Array(['Stardew Valley Almanac', 'Bait And Bobber', "Woodcutter's Weekly", 'Mining Monthly', 'Combat Quarterly']))
    if truth((binary('!==', e['offset'], '') if truth(_logic96 := (binary('!==', unary('typeof', e['offset']), 'undefined') if truth(_logic97 := e['isSearch']) else _logic97)) else _logic96)):
        call(get(call(e['$'], '#cart-prev-year'), 'prop'), 'disabled', True)
        call(get(call(e['$'], '#cart-prev-week'), 'prop'), 'disabled', True)
        call(get(call(e['$'], '#cart-next-week'), 'prop'), 'disabled', True)
        call(get(call(e['$'], '#cart-next-year'), 'prop'), 'disabled', True)
        call(get(call(e['$'], '#cart-reset'), 'html'), 'Clear Search Results &amp; Reset Browsing')
        e.set('searchTerm', call(e['RegExp'], e['offset'], 'i'))
        e.set('searchStart', (0 if truth(call(get(call(e['$'], '#cart-search-all'), 'prop'), 'checked')) else binary('*', 7, call(get(e['Math'], 'floor'), binary('/', binary('-', get(e['save'], 'daysPlayed'), 1), 7)))))
        e.set('searchEnd', binary('*', 112, call(get(call(e['$'], '#cart-search-range'), 'val'))))
        e.set('output', binary('+', e['output'], binary('+', binary('+', binary('+', binary('+', binary('+', '<table class="output"><thead><tr><th colspan="4">Search results for &quot;', e['offset']), '&quot; over the '), ('first ' if truth(call(get(call(e['$'], '#cart-search-all'), 'prop'), 'checked')) else 'next ')), call(get(call(e['$'], '#cart-search-range'), 'val'))), ' year(s)</th></tr>\n')))
        e.set('output', binary('+', e['output'], '<tr><th class="day">Day</th><th class="item">Item</th><th class="qty">Qty</th><th class="price">Price</th></tr>\n<tbody>'))
        e.set('count', 0)
        e.set('offset', e['searchStart'])
        while truth(binary('<', e['offset'], binary('+', e['searchStart'], e['searchEnd']))):
            e.set('days', Array([5, 7]))
            e.set('dayOfYear', binary('%', e['offset'], 112))
            if truth((_logic98 if truth(_logic98 := binary('===', e['dayOfYear'], 98)) else binary('===', e['dayOfYear'], 14))):
                e.set('days', Array([1, 2, 3, 5, 7]))
            e.set('month', call(get(e['Math'], 'floor'), binary('/', e['offset'], 28)))
            e.set('monthName', get(get(e['save'], 'seasonNames'), binary('%', e['month'], 4)))
            e.set('year', binary('+', 1, call(get(e['Math'], 'floor'), binary('/', e['offset'], 112))))
            e.set('i', 0)
            while truth(binary('<', e['i'], get(e['days'], 'length'))):
                e.set('seenRareSeed', False)
                e.set('dayOfMonth', binary('+', binary('%', e['offset'], 28), get(e['days'], e['i'])))
                e.set('dayOfWeek', get(get(e['save'], 'dayNames'), binary('-', get(e['days'], e['i']), 1)))
                e.set('rng', call(e['CSRandom'], call(e['getRandomSeed'], binary('+', binary('+', e['offset'], get(e['days'], e['i'])), get(e['save'], 'dayAdjust')), binary('/', get(e['save'], 'gameID'), 2))))
                e.set('pick', call(e['getRandomItems'], e['rng'], 'objects', 2, 789, True, True, True, 10))
                e.set('slot', 0)
                while truth(binary('<', e['slot'], 10)):
                    e.set('price', call(get(e['Math'], 'max'), binary('*', call(get(e['rng'], 'Next'), 1, 11), 100), binary('*', call(get(e['rng'], 'Next'), 3, 6), get(get(get(e['save'], 'objects'), get(e['pick'], e['slot'])), 'price'))))
                    e.set('qty', (5 if truth(binary('<', call(get(e['rng'], 'NextDouble')), 0.1)) else 1))
                    if truth(binary('===', get(get(get(e['save'], 'objects'), get(e['pick'], e['slot'])), 'name'), 'Rare Seed')):
                        e.set('seenRareSeed', True)
                    if truth(call(get(e['searchTerm'], 'test'), get(get(get(e['save'], 'objects'), get(e['pick'], e['slot'])), 'name'))):
                        update_env(e, 'count', 1, False)
                        e.set('output', binary('+', e['output'], binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', '<tr><td>', e['dayOfWeek']), ' '), e['monthName']), ' '), e['dayOfMonth']), ', Year '), e['year']), '</td><td>'), call(e['wikify'], get(get(get(e['save'], 'objects'), get(e['pick'], e['slot'])), 'name'))), '</td><td>'), e['qty']), '</td><td>'), call(e['addCommas'], e['price'])), 'g</td></tr>')))
                    update_env(e, 'slot', 1, False)
                if truth(binary('>=', get(e['save'], 'originalGuarantee'), 0)):
                    e.set('dayOfPrediction', binary('+', binary('+', e['offset'], get(e['days'], e['i'])), get(e['save'], 'dayAdjust')))
                    e.set('visitsNow', binary('-', binary('-', get(e['save'], 'originalGuarantee'), call(get(e['Math'], 'floor'), binary('/', e['dayOfPrediction'], 7))), call(get(e['Math'], 'floor'), binary('/', binary('+', e['dayOfPrediction'], 2), 7))))
                    if truth(binary('>=', e['dayOfPrediction'], 99)):
                        update_env(e, 'visitsNow', -1, False)
                    if truth(binary('>=', e['dayOfPrediction'], 100)):
                        update_env(e, 'visitsNow', -1, False)
                    if truth(binary('>=', e['dayOfPrediction'], 101)):
                        update_env(e, 'visitsNow', -1, False)
                    if truth(binary('==', e['visitsNow'], 0)):
                        e.set('name', get(get(get(e['save'], 'objects'), '_485'), 'name'))
                        e.set('price', call(get(e['Math'], 'max'), binary('*', call(get(e['rng'], 'Next'), 1, 11), 100), binary('*', call(get(e['rng'], 'Next'), 3, 6), get(get(get(e['save'], 'objects'), '_485'), 'price'))))
                        e.set('qty', (5 if truth(binary('<', call(get(e['rng'], 'NextDouble')), 0.1)) else 1))
                        if truth(call(get(e['searchTerm'], 'test'), e['name'])):
                            update_env(e, 'count', 1, False)
                            e.set('output', binary('+', e['output'], binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', '<tr><td>', e['dayOfWeek']), ' '), e['monthName']), ' '), e['dayOfMonth']), ', Year '), e['year']), '</td><td>'), call(e['wikify'], e['name'])), '</td><td>'), e['qty']), '</td><td>'), call(e['addCommas'], e['price'])), 'g</td></tr>')))
                e.set('pick', call(e['getRandomItems'], e['rng'], 'furniture', 0, 1612, True, True))
                e.set('name', get(get(get(e['save'], 'furniture'), get(e['pick'], 0)), 'name'))
                e.set('price', binary('*', call(get(e['rng'], 'Next'), 1, 11), 250))
                e.set('qty', 1)
                if truth(call(get(e['searchTerm'], 'test'), e['name'])):
                    update_env(e, 'count', 1, False)
                    e.set('output', binary('+', e['output'], binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', '<tr><td>', e['dayOfWeek']), ' '), e['monthName']), ' '), e['dayOfMonth']), ', Year '), e['year']), '</td><td>'), call(e['wikify'], e['name'], 'Furniture')), '</td><td>'), e['qty']), '</td><td>'), call(e['addCommas'], e['price'])), 'g</td></tr>')))
                if truth(binary('<', binary('%', e['month'], 4), 2)):
                    if truth(unary('!', e['seenRareSeed'])):
                        e.set('name', 'Rare Seed')
                        e.set('price', 1000)
                        e.set('qty', (5 if truth(binary('<', call(get(e['rng'], 'NextDouble')), 0.1)) else 1))
                        if truth(call(get(e['searchTerm'], 'test'), e['name'])):
                            update_env(e, 'count', 1, False)
                            e.set('output', binary('+', e['output'], binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', '<tr><td>', e['dayOfWeek']), ' '), e['monthName']), ' '), e['dayOfMonth']), ', Year '), e['year']), '</td><td>'), call(e['wikify'], e['name'])), '</td><td>'), e['qty']), '</td><td>'), call(e['addCommas'], e['price'])), 'g</td></tr>')))
                else:
                    e.set('rngSynced', call(e['CSRandom'], call(e['getRandomSeed'], call(e['getHashFromString'], 'cart_rarecrow'), get(e['save'], 'gameID'), binary('+', binary('+', e['offset'], get(e['days'], e['i'])), get(e['save'], 'dayAdjust')))))
                    e.set('name', 'Rarecrow (Snowman)')
                    if truth((call(get(e['searchTerm'], 'test'), e['name']) if truth(_logic99 := binary('<', call(get(e['rngSynced'], 'NextDouble')), 0.4)) else _logic99)):
                        e.set('price', 4000)
                        e.set('qty', 1)
                        update_env(e, 'count', 1, False)
                        e.set('output', binary('+', e['output'], binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', '<tr><td>', e['dayOfWeek']), ' '), e['monthName']), ' '), e['dayOfMonth']), ', Year '), e['year']), '</td><td>'), call(e['wikify'], e['name'])), '</td><td>'), e['qty']), '</td><td>'), call(e['addCommas'], e['price'])), 'g</td></tr>')))
                if truth(binary('>', binary('%', e['month'], 4), 1)):
                    e.set('rngSynced', call(e['CSRandom'], call(e['getRandomSeed'], call(e['getHashFromString'], 'cart_coffee_bean'), get(e['save'], 'gameID'), binary('+', binary('+', e['offset'], get(e['days'], e['i'])), get(e['save'], 'dayAdjust')))))
                    e.set('name', 'Coffee Bean')
                    if truth((call(get(e['searchTerm'], 'test'), e['name']) if truth(_logic100 := binary('<', call(get(e['rngSynced'], 'NextDouble')), 0.25)) else _logic100)):
                        e.set('price', 2500)
                        e.set('qty', 1)
                        update_env(e, 'count', 1, False)
                        e.set('output', binary('+', e['output'], binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', '<tr><td>', e['dayOfWeek']), ' '), e['monthName']), ' '), e['dayOfMonth']), ', Year '), e['year']), '</td><td>'), call(e['wikify'], e['name'])), '</td><td>'), e['qty']), '</td><td>'), call(e['addCommas'], e['price'])), 'g</td></tr>')))
                e.set('rngSynced', call(e['CSRandom'], call(e['getRandomSeed'], call(e['getHashFromString'], 'cart_fez'), get(e['save'], 'gameID'), binary('+', binary('+', e['offset'], get(e['days'], e['i'])), get(e['save'], 'dayAdjust')))))
                e.set('name', 'Red Fez')
                if truth((call(get(e['searchTerm'], 'test'), e['name']) if truth(_logic101 := binary('<', call(get(e['rngSynced'], 'NextDouble')), 0.1)) else _logic101)):
                    e.set('price', 8000)
                    e.set('qty', 1)
                    update_env(e, 'count', 1, False)
                    e.set('output', binary('+', e['output'], binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', '<tr><td>', e['dayOfWeek']), ' '), e['monthName']), ' '), e['dayOfMonth']), ', Year '), e['year']), '</td><td>'), call(e['wikify'], e['name'], 'Hats')), '</td><td>'), e['qty']), '</td><td>'), call(e['addCommas'], e['price'])), 'g</td></tr>')))
                if truth((_logic102 if truth(_logic102 := get(e['save'], 'ccComplete')) else get(e['save'], 'jojaComplete'))):
                    e.set('rngSynced', call(e['CSRandom'], call(e['getRandomSeed'], call(e['getHashFromString'], 'cart_jojaCatalogue'), get(e['save'], 'gameID'), binary('+', binary('+', e['offset'], get(e['days'], e['i'])), get(e['save'], 'dayAdjust')))))
                    e.set('name', 'Joja Catalogue')
                    if truth((call(get(e['searchTerm'], 'test'), e['name']) if truth(_logic103 := binary('<', call(get(e['rngSynced'], 'NextDouble')), 0.1)) else _logic103)):
                        e.set('price', 30000)
                        e.set('qty', 1)
                        update_env(e, 'count', 1, False)
                        e.set('output', binary('+', e['output'], binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', '<tr><td>', e['dayOfWeek']), ' '), e['monthName']), ' '), e['dayOfMonth']), ', Year '), e['year']), '</td><td>'), call(e['wikify'], e['name'])), '</td><td>'), e['qty']), '</td><td>'), call(e['addCommas'], e['price'])), 'g</td></tr>')))
                    e.set('rngSynced', call(e['CSRandom'], call(e['getRandomSeed'], call(e['getHashFromString'], 'cart_junimoCatalogue'), get(e['save'], 'gameID'), binary('+', binary('+', e['offset'], get(e['days'], e['i'])), get(e['save'], 'dayAdjust')))))
                    e.set('name', 'Junimo Catalogue')
                    if truth((call(get(e['searchTerm'], 'test'), e['name']) if truth(_logic104 := binary('<', call(get(e['rngSynced'], 'NextDouble')), 0.1)) else _logic104)):
                        e.set('price', 70000)
                        e.set('qty', 1)
                        update_env(e, 'count', 1, False)
                        e.set('output', binary('+', e['output'], binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', '<tr><td>', e['dayOfWeek']), ' '), e['monthName']), ' '), e['dayOfMonth']), ', Year '), e['year']), '</td><td>'), call(e['wikify'], e['name'])), '</td><td>'), e['qty']), '</td><td>'), call(e['addCommas'], e['price'])), 'g</td></tr>')))
                e.set('rngSynced', call(e['CSRandom'], call(e['getRandomSeed'], call(e['getHashFromString'], 'cart_retroCatalogue'), get(e['save'], 'gameID'), binary('+', binary('+', e['offset'], get(e['days'], e['i'])), get(e['save'], 'dayAdjust')))))
                e.set('name', 'Retro Catalogue')
                if truth((call(get(e['searchTerm'], 'test'), e['name']) if truth(_logic105 := binary('<', call(get(e['rngSynced'], 'NextDouble')), 0.1)) else _logic105)):
                    e.set('price', 110000)
                    e.set('qty', 1)
                    update_env(e, 'count', 1, False)
                    e.set('output', binary('+', e['output'], binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', '<tr><td>', e['dayOfWeek']), ' '), e['monthName']), ' '), e['dayOfMonth']), ', Year '), e['year']), '</td><td>'), call(e['wikify'], e['name'])), '</td><td>'), e['qty']), '</td><td>'), call(e['addCommas'], e['price'])), 'g</td></tr>')))
                e.set('rngSynced', call(e['CSRandom'], call(e['getRandomSeed'], call(e['getHashFromString'], 'teaset'), get(e['save'], 'gameID'), binary('+', binary('+', e['offset'], get(e['days'], e['i'])), get(e['save'], 'dayAdjust')))))
                e.set('name', 'Tea Set')
                if truth((binary('>=', binary('+', e['offset'], get(e['save'], 'dayAdjust')), 2688) if truth(_logic106 := (call(get(e['searchTerm'], 'test'), e['name']) if truth(_logic107 := binary('<', call(get(e['rngSynced'], 'NextDouble')), 0.1)) else _logic107)) else _logic106)):
                    e.set('price', 1000000)
                    e.set('qty', 1)
                    update_env(e, 'count', 1, False)
                    e.set('output', binary('+', e['output'], binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', '<tr><td>', e['dayOfWeek']), ' '), e['monthName']), ' '), e['dayOfMonth']), ', Year '), e['year']), '</td><td>'), call(e['wikify'], e['name'])), '</td><td>'), e['qty']), '</td><td>'), call(e['addCommas'], e['price'])), 'g</td></tr>')))
                update_env(e, 'i', 1, False)
            e.set('offset', binary('+', e['offset'], 7))
        e.set('output', binary('+', e['output'], binary('+', binary('+', '<tr><td colspan="4" class="count">Found ', e['count']), ' matching item(s)</td></tr></tbody></table>\n')))
    else:
        if truth((_logic108 if truth(_logic108 := binary('===', unary('typeof', e['offset']), 'undefined')) else binary('===', e['offset'], ''))):
            e.set('offset', binary('*', 7, call(get(e['Math'], 'floor'), binary('/', binary('-', get(e['save'], 'daysPlayed'), 1), 7))))
        e.set('dayOfYear', binary('%', e['offset'], 112))
        e.set('cartName', 'Forest Cart')
        e.set('nameOffset', 1)
        if truth((_logic109 if truth(_logic109 := binary('===', e['dayOfYear'], 94)) else binary('===', e['dayOfYear'], 10))):
            e.set('days', Array([5, 6, 7]))
            call(get(call(e['$'], '#cart-next-week'), 'val'), binary('+', e['offset'], 4))
            call(get(call(e['$'], '#cart-prev-week'), 'val'), binary('-', e['offset'], 3))
            e.set('nameOffset', 5)
            e.set('cartName', ('Night Market<br/>Boat' if truth(binary('===', e['dayOfYear'], 94)) else 'Desert Festival<br/>Cart'))
        else:
            e.set('days', Array([5, 7]))
            call(get(call(e['$'], '#cart-next-week'), 'val'), binary('+', e['offset'], 7))
            call(get(call(e['$'], '#cart-prev-week'), 'val'), binary('-', e['offset'], 7))
            if truth((_logic110 if truth(_logic110 := binary('===', e['dayOfYear'], 7)) else binary('===', e['dayOfYear'], 91))):
                call(get(call(e['$'], '#cart-next-week'), 'val'), binary('+', e['offset'], 3))
            if truth((_logic111 if truth(_logic111 := binary('===', e['dayOfYear'], 14)) else binary('===', e['dayOfYear'], 98))):
                call(get(call(e['$'], '#cart-prev-week'), 'val'), binary('-', e['offset'], 4))
        call(get(call(e['$'], '#cart-next-year'), 'val'), binary('+', e['offset'], 112))
        call(get(call(e['$'], '#cart-prev-year'), 'val'), binary('-', e['offset'], 112))
        if truth(binary('<', e['offset'], 7)):
            call(get(call(e['$'], '#cart-prev-week'), 'prop'), 'disabled', True)
        else:
            call(get(call(e['$'], '#cart-prev-week'), 'prop'), 'disabled', False)
        if truth(binary('<', e['offset'], 112)):
            call(get(call(e['$'], '#cart-prev-year'), 'prop'), 'disabled', True)
        else:
            call(get(call(e['$'], '#cart-prev-year'), 'prop'), 'disabled', False)
        call(get(call(e['$'], '#cart-reset'), 'val'), 'reset')
        call(get(call(e['$'], '#cart-reset'), 'html'), 'Reset Browsing')
        call(get(call(e['$'], '#cart-next-week'), 'prop'), 'disabled', False)
        call(get(call(e['$'], '#cart-next-year'), 'prop'), 'disabled', False)
        call(get(call(e['$'], '#cart-search-text'), 'val'), '')
        call(get(call(e['$'], '#cart-search-range'), 'val'), 2)
        call(get(call(e['$'], '#cart-search-all'), 'prop'), 'checked', False)
        e.set('month', call(get(e['Math'], 'floor'), binary('/', e['offset'], 28)))
        e.set('monthName', get(get(e['save'], 'seasonNames'), binary('%', e['month'], 4)))
        e.set('year', binary('+', 1, call(get(e['Math'], 'floor'), binary('/', e['offset'], 112))))
        e.set('dayOfMonth', binary('%', e['offset'], 28))
        e.set('output', binary('+', e['output'], binary('+', binary('+', '<table class="output"><thead><tr><th rowspan="2">', e['cartName']), '</th>')))
        e.set('d', 0)
        while truth(binary('<', e['d'], get(e['days'], 'length'))):
            e.set('output', binary('+', e['output'], binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', '<th colspan="3" class="multi">', get(get(e['save'], 'dayNames'), binary('-', get(e['days'], e['d']), e['nameOffset']))), ' '), e['monthName']), ' '), binary('+', e['dayOfMonth'], get(e['days'], e['d']))), ', Year '), e['year']), '</th>')))
            update_env(e, 'd', 1, False)
        e.set('output', binary('+', e['output'], '</tr><tr>'))
        e.set('d', 0)
        while truth(binary('<', e['d'], get(e['days'], 'length'))):
            e.set('output', binary('+', e['output'], '<th class="item">Item</th><th class="qty">Qty</th><th class="price">Price</th>'))
            update_env(e, 'd', 1, False)
        e.set('output', binary('+', e['output'], '</tr><tbody>'))
        e.set('cart', Obj({}))
        e.set('d', 0)
        while truth(binary('<', e['d'], get(e['days'], 'length'))):
            put(e['cart'], e['d'], Obj({}))
            put(get(e['cart'], e['d']), 'rng', call(e['CSRandom'], call(e['getRandomSeed'], binary('+', binary('+', e['offset'], get(e['days'], e['d'])), get(e['save'], 'dayAdjust')), binary('/', get(e['save'], 'gameID'), 2))))
            put(get(e['cart'], e['d']), 'seenRareSeed', False)
            put(get(e['cart'], e['d']), 'selectedItems', Obj({}))
            e.set('pick', call(e['getRandomItems'], get(get(e['cart'], e['d']), 'rng'), 'objects', 2, 789, True, True, True, 10))
            e.set('slot', 1)
            while truth(binary('<=', e['slot'], 10)):
                put(get(get(e['cart'], e['d']), 'selectedItems'), e['slot'], Obj({}))
                put(get(get(get(e['cart'], e['d']), 'selectedItems'), e['slot']), 'name', get(get(get(e['save'], 'objects'), get(e['pick'], binary('-', e['slot'], 1))), 'name'))
                if truth(binary('===', get(get(get(get(e['cart'], e['d']), 'selectedItems'), e['slot']), 'name'), 'Rare Seed')):
                    put(get(e['cart'], e['d']), 'seenRareSeed', True)
                put(get(get(get(e['cart'], e['d']), 'selectedItems'), e['slot']), 'price', call(get(e['Math'], 'max'), binary('*', call(get(get(get(e['cart'], e['d']), 'rng'), 'Next'), 1, 11), 100), binary('*', call(get(get(get(e['cart'], e['d']), 'rng'), 'Next'), 3, 6), get(get(get(e['save'], 'objects'), get(e['pick'], binary('-', e['slot'], 1))), 'price'))))
                put(get(get(get(e['cart'], e['d']), 'selectedItems'), e['slot']), 'qty', (5 if truth(binary('<', call(get(get(get(e['cart'], e['d']), 'rng'), 'NextDouble')), 0.1)) else 1))
                update_env(e, 'slot', 1, False)
            update_env(e, 'd', 1, False)
        e.set('slot', 1)
        while truth(binary('<=', e['slot'], 10)):
            e.set('output', binary('+', e['output'], binary('+', binary('+', '<tr><td>Basic Item ', e['slot']), '</td>')))
            e.set('d', 0)
            while truth(binary('<', e['d'], get(e['days'], 'length'))):
                e.set('output', binary('+', e['output'], binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', '<td class="item">', call(e['wikify'], get(get(get(get(e['cart'], e['d']), 'selectedItems'), e['slot']), 'name'))), '</td><td>'), get(get(get(get(e['cart'], e['d']), 'selectedItems'), e['slot']), 'qty')), '</td><td>'), call(e['addCommas'], get(get(get(get(e['cart'], e['d']), 'selectedItems'), e['slot']), 'price'))), 'g</td>')))
                update_env(e, 'd', 1, False)
            e.set('output', binary('+', e['output'], '</tr>'))
            update_env(e, 'slot', 1, False)
        if truth(binary('>=', get(e['save'], 'originalGuarantee'), 0)):
            e.set('output', binary('+', e['output'], '<tr><td>Year 1 Guarantee</td>'))
            e.set('d', 0)
            while truth(binary('<', e['d'], get(e['days'], 'length'))):
                e.set('dayOfPrediction', binary('+', binary('+', e['offset'], get(e['days'], e['d'])), get(e['save'], 'dayAdjust')))
                e.set('visitsNow', binary('-', binary('-', get(e['save'], 'originalGuarantee'), call(get(e['Math'], 'floor'), binary('/', e['dayOfPrediction'], 7))), call(get(e['Math'], 'floor'), binary('/', binary('+', e['dayOfPrediction'], 2), 7))))
                if truth(binary('>=', e['dayOfPrediction'], 99)):
                    update_env(e, 'visitsNow', -1, False)
                if truth(binary('>=', e['dayOfPrediction'], 100)):
                    update_env(e, 'visitsNow', -1, False)
                if truth(binary('>=', e['dayOfPrediction'], 101)):
                    update_env(e, 'visitsNow', -1, False)
                if truth(binary('==', e['visitsNow'], 0)):
                    e.set('name', get(get(get(e['save'], 'objects'), '_485'), 'name'))
                    e.set('price', call(get(e['Math'], 'max'), binary('*', call(get(get(get(e['cart'], e['d']), 'rng'), 'Next'), 1, 11), 100), binary('*', call(get(get(get(e['cart'], e['d']), 'rng'), 'Next'), 3, 6), get(get(get(e['save'], 'objects'), '_485'), 'price'))))
                    e.set('qty', (5 if truth(binary('<', call(get(get(get(e['cart'], e['d']), 'rng'), 'NextDouble')), 0.1)) else 1))
                    e.set('output', binary('+', e['output'], binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', '<td class="item">', call(e['wikify'], e['name'])), '</td><td>'), e['qty']), '</td><td>'), call(e['addCommas'], e['price'])), 'g</td>')))
                else:
                    if truth(binary('>', e['visitsNow'], 0)):
                        e.set('output', binary('+', e['output'], binary('+', binary('+', binary('+', '<td class="item">(', e['visitsNow']), (' visit' if truth(binary('==', e['visitsNow'], 1)) else ' visits')), ' left)</td><td>--</td><td>--</td>')))
                    else:
                        e.set('output', binary('+', e['output'], '<td class="item">(Already passed)</td><td>--</td><td>--</td>'))
                update_env(e, 'd', 1, False)
            e.set('output', binary('+', e['output'], '</tr>'))
        e.set('output', binary('+', e['output'], '<tr><td>Furniture</td>'))
        e.set('d', 0)
        while truth(binary('<', e['d'], get(e['days'], 'length'))):
            e.set('pick', call(e['getRandomItems'], get(get(e['cart'], e['d']), 'rng'), 'furniture', 0, 1612, True, True))
            e.set('name', get(get(get(e['save'], 'furniture'), get(e['pick'], 0)), 'name'))
            e.set('price', binary('*', call(get(get(get(e['cart'], e['d']), 'rng'), 'Next'), 1, 11), 250))
            e.set('output', binary('+', e['output'], binary('+', binary('+', binary('+', binary('+', '<td class="item">', call(e['wikify'], e['name'], 'Furniture')), '</td><td>1</td><td>'), call(e['addCommas'], e['price'])), 'g</td>')))
            update_env(e, 'd', 1, False)
        e.set('output', binary('+', e['output'], '</tr>'))
        e.set('output', binary('+', e['output'], '<tr><td>Seasonal Special</td>'))
        if truth(binary('<', binary('%', e['month'], 4), 2)):
            e.set('d', 0)
            while truth(binary('<', e['d'], get(e['days'], 'length'))):
                if truth(unary('!', get(get(e['cart'], e['d']), 'seenRareSeed'))):
                    e.set('name', call(e['wikify'], 'Rare Seed'))
                    e.set('price', 1000)
                    e.set('qty', (5 if truth(binary('<', call(get(get(get(e['cart'], e['d']), 'rng'), 'NextDouble')), 0.1)) else 1))
                else:
                    e.set('name', '(None)')
                    e.set('price', '--')
                    e.set('qty', '--')
                e.set('output', binary('+', e['output'], binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', '<td class="item">', e['name']), '</td><td>'), e['qty']), '</td><td>'), call(e['addCommas'], e['price'])), ('' if truth(binary('==', e['price'], '--')) else 'g')), '</td>')))
                update_env(e, 'd', 1, False)
        else:
            e.set('d', 0)
            while truth(binary('<', e['d'], get(e['days'], 'length'))):
                e.set('rngSynced', call(e['CSRandom'], call(e['getRandomSeed'], call(e['getHashFromString'], 'cart_rarecrow'), get(e['save'], 'gameID'), binary('+', binary('+', e['offset'], get(e['days'], e['d'])), get(e['save'], 'dayAdjust')))))
                if truth(binary('<', call(get(e['rngSynced'], 'NextDouble')), 0.4)):
                    e.set('name', call(e['wikify'], 'Rarecrow (Snowman)'))
                    e.set('price', 4000)
                    e.set('qty', 1)
                else:
                    e.set('name', '(None)')
                    e.set('price', '--')
                    e.set('qty', '--')
                e.set('output', binary('+', e['output'], binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', '<td class="item">', e['name']), '</td><td>'), e['qty']), '</td><td>'), call(e['addCommas'], e['price'])), ('' if truth(binary('==', e['price'], '--')) else 'g')), '</td>')))
                update_env(e, 'd', 1, False)
        e.set('output', binary('+', e['output'], '</tr>'))
        e.set('output', binary('+', e['output'], '<tr><td>Coffee Bean</td>'))
        if truth(binary('>', binary('%', e['month'], 4), 1)):
            e.set('d', 0)
            while truth(binary('<', e['d'], get(e['days'], 'length'))):
                e.set('rngSynced', call(e['CSRandom'], call(e['getRandomSeed'], call(e['getHashFromString'], 'cart_coffee_bean'), get(e['save'], 'gameID'), binary('+', binary('+', e['offset'], get(e['days'], e['d'])), get(e['save'], 'dayAdjust')))))
                if truth(binary('<', call(get(e['rngSynced'], 'NextDouble')), 0.25)):
                    e.set('name', call(e['wikify'], 'Coffee Bean'))
                    e.set('price', 2500)
                    e.set('qty', 1)
                else:
                    e.set('name', '(None)')
                    e.set('price', '--')
                    e.set('qty', '--')
                e.set('output', binary('+', e['output'], binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', '<td class="item">', e['name']), '</td><td>'), e['qty']), '</td><td>'), call(e['addCommas'], e['price'])), ('' if truth(binary('==', e['price'], '--')) else 'g')), '</td>')))
                update_env(e, 'd', 1, False)
        else:
            e.set('span', binary('*', get(e['days'], 'length'), 3))
            e.set('output', binary('+', e['output'], binary('+', binary('+', '<td class="item note" colspan="', e['span']), '">Only possible in Fall or Winter</td>')))
        e.set('output', binary('+', e['output'], '</tr>'))
        e.set('output', binary('+', e['output'], '<tr><td>Red Fez</td>'))
        e.set('d', 0)
        while truth(binary('<', e['d'], get(e['days'], 'length'))):
            e.set('rngSynced', call(e['CSRandom'], call(e['getRandomSeed'], call(e['getHashFromString'], 'cart_fez'), get(e['save'], 'gameID'), binary('+', binary('+', e['offset'], get(e['days'], e['d'])), get(e['save'], 'dayAdjust')))))
            if truth(binary('<', call(get(e['rngSynced'], 'NextDouble')), 0.1)):
                e.set('name', call(e['wikify'], 'Red Fez'))
                e.set('price', 8000)
                e.set('qty', 1)
            else:
                e.set('name', '(None)')
                e.set('price', '--')
                e.set('qty', '--')
            e.set('output', binary('+', e['output'], binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', '<td class="item">', e['name']), '</td><td>'), e['qty']), '</td><td>'), call(e['addCommas'], e['price'])), ('' if truth(binary('==', e['price'], '--')) else 'g')), '</td>')))
            update_env(e, 'd', 1, False)
        e.set('output', binary('+', e['output'], '</tr>'))
        e.set('output', binary('+', e['output'], '<tr><td>Catalogue 1</td>'))
        if truth(get(e['save'], 'ccComplete')):
            e.set('d', 0)
            while truth(binary('<', e['d'], get(e['days'], 'length'))):
                e.set('rngSynced', call(e['CSRandom'], call(e['getRandomSeed'], call(e['getHashFromString'], 'cart_jojaCatalogue'), get(e['save'], 'gameID'), binary('+', binary('+', e['offset'], get(e['days'], e['d'])), get(e['save'], 'dayAdjust')))))
                if truth(binary('<', call(get(e['rngSynced'], 'NextDouble')), 0.1)):
                    e.set('name', call(e['wikify'], 'Joja Catalogue'))
                    e.set('price', 30000)
                    e.set('qty', 1)
                else:
                    e.set('name', '(None)')
                    e.set('price', '--')
                    e.set('qty', '--')
                e.set('output', binary('+', e['output'], binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', '<td class="item">', e['name']), '</td><td>'), e['qty']), '</td><td>'), call(e['addCommas'], e['price'])), ('' if truth(binary('==', e['price'], '--')) else 'g')), '</td>')))
                update_env(e, 'd', 1, False)
        else:
            e.set('span', binary('*', get(e['days'], 'length'), 3))
            e.set('output', binary('+', e['output'], binary('+', binary('+', '<td class="item note" colspan="', e['span']), '">Only possible after Community Center Restoration</td>')))
        e.set('output', binary('+', e['output'], '</tr>'))
        e.set('output', binary('+', e['output'], '<tr><td>Catalogue 2</td>'))
        if truth((_logic112 if truth(_logic112 := get(e['save'], 'ccComplete')) else get(e['save'], 'jojaComplete'))):
            e.set('d', 0)
            while truth(binary('<', e['d'], get(e['days'], 'length'))):
                e.set('rngSynced', call(e['CSRandom'], call(e['getRandomSeed'], call(e['getHashFromString'], 'cart_junimoCatalogue'), get(e['save'], 'gameID'), binary('+', binary('+', e['offset'], get(e['days'], e['d'])), get(e['save'], 'dayAdjust')))))
                if truth(binary('<', call(get(e['rngSynced'], 'NextDouble')), 0.1)):
                    e.set('name', call(e['wikify'], 'Junimo Catalogue'))
                    e.set('price', 70000)
                    e.set('qty', 1)
                else:
                    e.set('name', '(None)')
                    e.set('price', '--')
                    e.set('qty', '--')
                e.set('output', binary('+', e['output'], binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', '<td class="item">', e['name']), '</td><td>'), e['qty']), '</td><td>'), call(e['addCommas'], e['price'])), ('' if truth(binary('==', e['price'], '--')) else 'g')), '</td>')))
                update_env(e, 'd', 1, False)
        else:
            e.set('span', binary('*', get(e['days'], 'length'), 3))
            e.set('output', binary('+', e['output'], binary('+', binary('+', '<td class="item note" colspan="', e['span']), '">Only possible after Community Center Restoration</td>')))
        e.set('output', binary('+', e['output'], '</tr>'))
        e.set('output', binary('+', e['output'], '<tr><td>Catalogue 3</td>'))
        e.set('d', 0)
        while truth(binary('<', e['d'], get(e['days'], 'length'))):
            e.set('rngSynced', call(e['CSRandom'], call(e['getRandomSeed'], call(e['getHashFromString'], 'cart_retroCatalogue'), get(e['save'], 'gameID'), binary('+', binary('+', e['offset'], get(e['days'], e['d'])), get(e['save'], 'dayAdjust')))))
            if truth(binary('<', call(get(e['rngSynced'], 'NextDouble')), 0.1)):
                e.set('name', call(e['wikify'], 'Retro Catalogue'))
                e.set('price', 110000)
                e.set('qty', 1)
            else:
                e.set('name', '(None)')
                e.set('price', '--')
                e.set('qty', '--')
            e.set('output', binary('+', e['output'], binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', '<td class="item">', e['name']), '</td><td>'), e['qty']), '</td><td>'), call(e['addCommas'], e['price'])), ('' if truth(binary('==', e['price'], '--')) else 'g')), '</td>')))
            update_env(e, 'd', 1, False)
        e.set('output', binary('+', e['output'], '</tr>'))
        e.set('output', binary('+', e['output'], '<tr><td>Y25 Tea Set</td>'))
        if truth(binary('>=', binary('+', e['offset'], get(e['save'], 'dayAdjust')), 2688)):
            e.set('d', 0)
            while truth(binary('<', e['d'], get(e['days'], 'length'))):
                e.set('rngSynced', call(e['CSRandom'], call(e['getRandomSeed'], call(e['getHashFromString'], 'teaset'), get(e['save'], 'gameID'), binary('+', binary('+', e['offset'], get(e['days'], e['d'])), get(e['save'], 'dayAdjust')))))
                if truth(binary('<', call(get(e['rngSynced'], 'NextDouble')), 0.05)):
                    e.set('name', call(e['wikify'], 'Tea Set'))
                    e.set('price', 1000000)
                    e.set('qty', '∞')
                else:
                    e.set('name', '(None)')
                    e.set('price', '--')
                    e.set('qty', '--')
                e.set('output', binary('+', e['output'], binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', '<td class="item">', e['name']), '</td><td>'), e['qty']), '</td><td>'), call(e['addCommas'], e['price'])), ('' if truth(binary('==', e['price'], '--')) else 'g')), '</td>')))
                update_env(e, 'd', 1, False)
        else:
            e.set('span', binary('*', get(e['days'], 'length'), 3))
            e.set('output', binary('+', e['output'], binary('+', binary('+', '<td class="item note" colspan="', e['span']), '">Only possible in Year 25 or later</td>')))
        e.set('output', binary('+', e['output'], '</tr>'))
        e.set('output', binary('+', e['output'], '<tr><td>Skill Book</td>'))
        e.set('d', 0)
        while truth(binary('<', e['d'], get(e['days'], 'length'))):
            e.set('rngSynced', call(e['CSRandom'], call(e['getRandomSeed'], call(e['getHashFromString'], 'travelerSkillBook'), get(e['save'], 'gameID'), binary('+', binary('+', e['offset'], get(e['days'], e['d'])), get(e['save'], 'dayAdjust')))))
            if truth(binary('<', call(get(e['rngSynced'], 'NextDouble')), 0.05)):
                e.set('name', call(e['wikify'], get(e['skillBookList'], call(get(get(get(e['cart'], e['d']), 'rng'), 'Next'), get(e['skillBookList'], 'length')))))
                e.set('price', 6000)
                e.set('qty', 1)
            else:
                e.set('name', '(None)')
                e.set('price', '--')
                e.set('qty', '--')
            e.set('output', binary('+', e['output'], binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', '<td class="book item">', e['name']), '</td><td>'), e['qty']), '</td><td>'), call(e['addCommas'], e['price'])), ('' if truth(binary('==', e['price'], '--')) else 'g')), '</td>')))
            update_env(e, 'd', 1, False)
        e.set('output', binary('+', e['output'], '</tr>'))
        e.set('output', binary('+', e['output'], '</tbody></table>\n'))
    return e['output']
    return U


def predictKrobus_113(parent, this, args):
    # Upstream predictor: 5493
    e = Env(parent)
    e.declare(['count', 'dayOfMonth', 'dayOfWeek', 'days', 'i', 'item', 'month', 'monthName', 'output', 'price', 'qty', 'result', 'rng', 'rngSynced', 'searchEnd', 'searchStart', 'searchTerm', 'thisRoll', 'year'])
    e.local['arguments'] = Array(args)
    e.local['isSearch'] = (args[0] if len(args) > 0 and args[0] is not U else U)
    e.local['offset'] = (args[1] if len(args) > 1 and args[1] is not U else U)
    e.set('output', '')
    if truth((binary('!==', e['offset'], '') if truth(_logic114 := (binary('!==', unary('typeof', e['offset']), 'undefined') if truth(_logic115 := e['isSearch']) else _logic115)) else _logic114)):
        call(get(call(e['$'], '#krobus-prev-year'), 'prop'), 'disabled', True)
        call(get(call(e['$'], '#krobus-prev-week'), 'prop'), 'disabled', True)
        call(get(call(e['$'], '#krobus-next-week'), 'prop'), 'disabled', True)
        call(get(call(e['$'], '#krobus-next-year'), 'prop'), 'disabled', True)
        call(get(call(e['$'], '#krobus-reset'), 'html'), 'Clear Search Results &amp; Reset Browsing')
        e.set('searchTerm', call(e['RegExp'], e['offset'], 'i'))
        e.set('searchStart', (0 if truth(call(get(call(e['$'], '#krobus-search-all'), 'prop'), 'checked')) else binary('*', 7, call(get(e['Math'], 'floor'), binary('/', binary('-', get(e['save'], 'daysPlayed'), 1), 7)))))
        e.set('searchEnd', binary('*', 112, call(get(call(e['$'], '#krobus-search-range'), 'val'))))
        e.set('output', binary('+', e['output'], binary('+', binary('+', binary('+', binary('+', binary('+', '<table class="output"><thead><tr><th colspan="4">Search results for &quot;', e['offset']), '&quot; over the '), ('first ' if truth(call(get(call(e['$'], '#krobus-search-all'), 'prop'), 'checked')) else 'next ')), call(get(call(e['$'], '#krobus-search-range'), 'val'))), ' year(s)</th></tr>\n')))
        e.set('output', binary('+', e['output'], '<tr><th class="day">Day</th><th class="item">Item</th><th class="qty">Qty</th><th class="price">Price</th></tr>\n<tbody>'))
        e.set('count', 0)
        e.set('qty', 5)
        e.set('offset', e['searchStart'])
        while truth(binary('<', e['offset'], binary('+', e['searchStart'], e['searchEnd']))):
            e.set('days', Array([3, 6]))
            e.set('i', 0)
            while truth(binary('<', e['i'], get(e['days'], 'length'))):
                if truth(binary('>=', call(e['compareSemVer'], get(e['save'], 'version'), '1.6'), 0)):
                    e.set('rng', call(e['CSRandom'], call(e['getRandomSeed'], binary('+', binary('+', e['offset'], get(e['days'], e['i'])), get(e['save'], 'dayAdjust')), binary('/', get(e['save'], 'gameID'), 2))))
                    if truth(binary('===', get(e['days'], e['i']), 3)):
                        e.set('result', call(e['getRandomItems'], e['rng'], 'objects', 698, 708, True, True))
                        e.set('item', get(get(get(e['save'], 'objects'), get(e['result'], 0)), 'name'))
                        e.set('price', 200)
                    else:
                        if truth(binary('===', get(e['days'], e['i']), 6)):
                            e.set('rngSynced', call(e['CSRandom'], call(e['getRandomSeed'], call(e['getHashFromString'], 'krobus_bread'), binary('+', binary('+', e['offset'], get(e['days'], e['i'])), get(e['save'], 'dayAdjust')))))
                            if truth(binary('<', call(get(e['rngSynced'], 'NextDouble')), 0.0196078431)):
                                e.set('item', get(get(get(e['save'], 'objects'), '_216'), 'name'))
                                e.set('price', binary('*', 10, call(get(e['rng'], 'Next'), 5, 51)))
                            else:
                                e.set('result', call(e['getRandomItems'], e['rng'], 'objects', 194, 244, True, True))
                                e.set('item', get(get(get(e['save'], 'objects'), get(e['result'], 0)), 'name'))
                                e.set('price', binary('*', 10, call(get(e['rng'], 'Next'), 5, 51)))
                else:
                    e.set('rng', call(e['CSRandom'], binary('+', binary('+', binary('+', binary('/', get(e['save'], 'gameID'), 2), e['offset']), get(e['days'], e['i'])), get(e['save'], 'dayAdjust'))))
                    if truth(binary('===', get(e['days'], e['i']), 3)):
                        e.set('item', get(get(e['save'], 'cartItems'), binary('-', call(get(e['rng'], 'Next'), 698, 709), 1)))
                        e.set('price', 200)
                    else:
                        if truth(binary('===', get(e['days'], e['i']), 6)):
                            e.set('thisRoll', binary('-', call(get(e['rng'], 'Next'), 194, 245), 1))
                            if truth(binary('===', e['thisRoll'], 216)):
                                e.set('thisRoll', 215)
                            e.set('item', get(get(e['save'], 'cartItems'), e['thisRoll']))
                            e.set('price', binary('*', call(get(e['rng'], 'Next'), 5, 51), 10))
                if truth(call(get(e['searchTerm'], 'test'), e['item'])):
                    update_env(e, 'count', 1, False)
                    e.set('month', call(get(e['Math'], 'floor'), binary('/', e['offset'], 28)))
                    e.set('monthName', get(get(e['save'], 'seasonNames'), binary('%', e['month'], 4)))
                    e.set('year', binary('+', 1, call(get(e['Math'], 'floor'), binary('/', e['offset'], 112))))
                    e.set('dayOfMonth', binary('+', binary('%', e['offset'], 28), get(e['days'], e['i'])))
                    e.set('dayOfWeek', get(get(e['save'], 'dayNames'), binary('-', get(e['days'], e['i']), 1)))
                    e.set('output', binary('+', e['output'], binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', '<tr><td>', e['dayOfWeek']), ' '), e['monthName']), ' '), e['dayOfMonth']), ', Year '), e['year']), '</td><td>'), call(e['wikify'], e['item'])), '</td><td>'), e['qty']), '</td><td>'), e['price']), 'g</td>')))
                update_env(e, 'i', 1, False)
            e.set('offset', binary('+', e['offset'], 7))
        e.set('output', binary('+', e['output'], binary('+', binary('+', '<tr><td colspan="4" class="count">Found ', e['count']), ' matching item(s)</td></tr></tbody></table>\n')))
    else:
        if truth((_logic116 if truth(_logic116 := binary('===', unary('typeof', e['offset']), 'undefined')) else binary('===', e['offset'], ''))):
            e.set('offset', binary('*', 7, call(get(e['Math'], 'floor'), binary('/', binary('-', get(e['save'], 'daysPlayed'), 1), 7))))
        call(get(call(e['$'], '#krobus-prev-year'), 'val'), binary('-', e['offset'], 112))
        call(get(call(e['$'], '#krobus-prev-week'), 'val'), binary('-', e['offset'], 7))
        call(get(call(e['$'], '#krobus-next-week'), 'val'), binary('+', e['offset'], 7))
        call(get(call(e['$'], '#krobus-next-year'), 'val'), binary('+', e['offset'], 112))
        if truth(binary('<', e['offset'], 7)):
            call(get(call(e['$'], '#krobus-prev-week'), 'prop'), 'disabled', True)
        else:
            call(get(call(e['$'], '#krobus-prev-week'), 'prop'), 'disabled', False)
        if truth(binary('<', e['offset'], 112)):
            call(get(call(e['$'], '#krobus-prev-year'), 'prop'), 'disabled', True)
        else:
            call(get(call(e['$'], '#krobus-prev-year'), 'prop'), 'disabled', False)
        call(get(call(e['$'], '#krobus-reset'), 'val'), 'reset')
        call(get(call(e['$'], '#krobus-reset'), 'html'), 'Reset Browsing')
        call(get(call(e['$'], '#krobus-next-week'), 'prop'), 'disabled', False)
        call(get(call(e['$'], '#krobus-next-year'), 'prop'), 'disabled', False)
        call(get(call(e['$'], '#krobus-search-text'), 'val'), '')
        call(get(call(e['$'], '#krobus-search-range'), 'val'), 2)
        call(get(call(e['$'], '#krobus-search-all'), 'prop'), 'checked', False)
        e.set('month', call(get(e['Math'], 'floor'), binary('/', e['offset'], 28)))
        e.set('monthName', get(get(e['save'], 'seasonNames'), binary('%', e['month'], 4)))
        e.set('year', binary('+', 1, call(get(e['Math'], 'floor'), binary('/', e['offset'], 112))))
        e.set('dayOfMonth', binary('%', e['offset'], 28))
        e.set('output', binary('+', e['output'], binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', '<table class="output"><thead><tr><th colspan="3" class="multi">', get(get(e['save'], 'dayNames'), 2)), ' '), e['monthName']), ' '), binary('+', e['dayOfMonth'], 3)), ', Year '), e['year']), '</th>')))
        e.set('output', binary('+', e['output'], binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', '<th colspan="3" class="multi">', get(get(e['save'], 'dayNames'), 5)), ' '), e['monthName']), ' '), binary('+', e['dayOfMonth'], 6)), ', Year '), e['year']), '</th></tr>\n')))
        e.set('output', binary('+', e['output'], '<tr><th class="item">Item</th><th class="qty">Qty</th><th class="price">Price</th>'))
        e.set('output', binary('+', e['output'], '<th class="item">Item</th><th class="qty">Qty</th><th class="price">Price</th></tr>\n<tbody><tr>'))
        e.set('item', Array(['None', 'None']))
        e.set('price', Array([200, 0]))
        e.set('qty', Array([5, 5]))
        if truth(binary('>=', call(e['compareSemVer'], get(e['save'], 'version'), '1.6'), 0)):
            e.set('rng', call(e['CSRandom'], call(e['getRandomSeed'], binary('+', binary('+', e['offset'], 3), get(e['save'], 'dayAdjust')), binary('/', get(e['save'], 'gameID'), 2))))
            e.set('result', call(e['getRandomItems'], e['rng'], 'objects', 698, 708, True, True))
            put(e['item'], 0, get(get(get(e['save'], 'objects'), get(e['result'], 0)), 'name'))
            e.set('rng', call(e['CSRandom'], call(e['getRandomSeed'], binary('+', binary('+', e['offset'], 6), get(e['save'], 'dayAdjust')), binary('/', get(e['save'], 'gameID'), 2))))
            e.set('rngSynced', call(e['CSRandom'], call(e['getRandomSeed'], call(e['getHashFromString'], 'krobus_bread'), binary('+', binary('+', e['offset'], 6), get(e['save'], 'dayAdjust')))))
            if truth(binary('<', call(get(e['rngSynced'], 'NextDouble')), 0.0196078431)):
                put(e['item'], 1, get(get(get(e['save'], 'objects'), '_216'), 'name'))
                put(e['price'], 1, binary('*', 10, call(get(e['rng'], 'Next'), 5, 51)))
            else:
                e.set('result', call(e['getRandomItems'], e['rng'], 'objects', 194, 244, True, True))
                put(e['item'], 1, get(get(get(e['save'], 'objects'), get(e['result'], 0)), 'name'))
                put(e['price'], 1, binary('*', 10, call(get(e['rng'], 'Next'), 5, 51)))
        else:
            e.set('rng', call(e['CSRandom'], binary('+', binary('+', binary('+', binary('/', get(e['save'], 'gameID'), 2), e['offset']), 3), get(e['save'], 'dayAdjust'))))
            put(e['item'], 0, get(get(e['save'], 'cartItems'), binary('-', call(get(e['rng'], 'Next'), 698, 709), 1)))
            e.set('rng', call(e['CSRandom'], binary('+', binary('+', binary('+', binary('/', get(e['save'], 'gameID'), 2), e['offset']), 6), get(e['save'], 'dayAdjust'))))
            e.set('thisRoll', binary('-', call(get(e['rng'], 'Next'), 194, 245), 1))
            if truth(binary('===', e['thisRoll'], 216)):
                e.set('thisRoll', 215)
            put(e['item'], 1, get(get(e['save'], 'cartItems'), e['thisRoll']))
            put(e['price'], 1, binary('*', call(get(e['rng'], 'Next'), 5, 51), 10))
        e.set('i', 0)
        while truth(binary('<', e['i'], get(e['item'], 'length'))):
            e.set('output', binary('+', e['output'], binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', '<td class="item">', call(e['wikify'], get(e['item'], e['i']))), '</td><td>'), get(e['qty'], e['i'])), '</td><td>'), call(e['addCommas'], get(e['price'], e['i']))), 'g</td>')))
            update_env(e, 'i', 1, False)
        e.set('output', binary('+', e['output'], '</tr></tbody></table>\n'))
    return e['output']
    return U


def predictSandy_117(parent, this, args):
    # Upstream predictor: 5652
    e = Env(parent)
    e.declare(['ccShirts', 'count', 'day', 'dayOfMonth', 'dayOfWeek', 'extra', 'i', 'item', 'month', 'monthName', 'numID', 'oasisShirts', 'output', 'result', 'rng', 'searchEnd', 'searchStart', 'searchTerm', 'spriteID', 'tclass', 'thisRoll', 'year'])
    e.local['arguments'] = Array(args)
    e.local['isSearch'] = (args[0] if len(args) > 0 and args[0] is not U else U)
    e.local['offset'] = (args[1] if len(args) > 1 and args[1] is not U else U)
    e.set('output', '')
    e.set('ccShirts', Array([1019, 1022, 1023, 1040, 1041, 1043, 1045, 1046, 1049, 1054, 1056, 1060, 1076, 1080, 1082, 1084, 1087, 1090, 1108, 1109, 1110]))
    e.set('oasisShirts', Array([1118, 1119, 1120, 1121]))
    if truth((binary('!==', e['offset'], '') if truth(_logic118 := (binary('!==', unary('typeof', e['offset']), 'undefined') if truth(_logic119 := e['isSearch']) else _logic119)) else _logic118)):
        call(get(call(e['$'], '#sandy-prev-year'), 'prop'), 'disabled', True)
        call(get(call(e['$'], '#sandy-prev-week'), 'prop'), 'disabled', True)
        call(get(call(e['$'], '#sandy-next-week'), 'prop'), 'disabled', True)
        call(get(call(e['$'], '#sandy-next-year'), 'prop'), 'disabled', True)
        call(get(call(e['$'], '#sandy-reset'), 'html'), 'Clear Search Results &amp; Reset Browsing')
        e.set('searchTerm', call(e['RegExp'], e['offset'], 'i'))
        e.set('searchStart', (1 if truth(call(get(call(e['$'], '#sandy-search-all'), 'prop'), 'checked')) else binary('*', 7, call(get(e['Math'], 'floor'), binary('/', binary('-', get(e['save'], 'daysPlayed'), 1), 7)))))
        e.set('searchEnd', binary('*', 112, call(get(call(e['$'], '#sandy-search-range'), 'val'))))
        e.set('output', binary('+', e['output'], binary('+', binary('+', binary('+', binary('+', binary('+', '<table class="output"><thead><tr><th colspan="3">Search results for &quot;', e['offset']), '&quot; over the '), ('first ' if truth(call(get(call(e['$'], '#sandy-search-all'), 'prop'), 'checked')) else 'next ')), call(get(call(e['$'], '#sandy-search-range'), 'val'))), ' year(s)</th></tr>\n')))
        e.set('output', binary('+', e['output'], '<tr><th class="day">Day</th><th class="shirt-item">Image</th><th class="item">Name</th></tr>\n<tbody>'))
        e.set('count', 0)
        call(get(e['console'], 'log'), binary('+', binary('+', binary('+', 'Searching from ', e['searchStart']), ' to '), binary('+', e['searchStart'], e['searchEnd'])))
        e.set('offset', e['searchStart'])
        while truth(binary('<', e['offset'], binary('+', e['searchStart'], e['searchEnd']))):
            e.set('i', 0)
            while truth(binary('<', e['i'], 7)):
                e.set('day', binary('+', e['offset'], e['i']))
                e.set('extra', '')
                e.set('numID', 0)
                if truth(binary('>=', call(e['compareSemVer'], get(e['save'], 'version'), '1.6'), 0)):
                    e.set('rng', call(e['CSRandom'], call(e['getRandomSeed'], binary('+', e['day'], get(e['save'], 'dayAdjust')), binary('/', get(e['save'], 'gameID'), 2))))
                    e.set('result', call(e['getRandomItems'], e['rng'], 'shirts', 1000, 1126, True, True))
                    e.set('spriteID', binary('-', get(get(get(e['save'], 'shirts'), get(e['result'], 0)), 'id'), 999))
                    e.set('numID', call(e['Number'], get(get(get(e['save'], 'shirts'), get(e['result'], 0)), 'id')))
                    e.set('item', binary('+', binary('+', binary('+', get(get(get(e['save'], 'shirts'), get(e['result'], 0)), 'name'), " (ID '(S)"), get(get(get(e['save'], 'shirts'), get(e['result'], 0)), 'id')), "')"))
                else:
                    e.set('rng', call(e['CSRandom'], binary('+', binary('+', binary('/', get(e['save'], 'gameID'), 2), e['day']), get(e['save'], 'dayAdjust'))))
                    e.set('thisRoll', binary('+', 1000, call(get(e['rng'], 'Next'), 127)))
                    e.set('spriteID', binary('-', e['thisRoll'], 999))
                    e.set('numID', e['thisRoll'])
                    e.set('item', binary('+', binary('+', binary('+', get(get(get(e['save'], 'shirts'), binary('+', '_', e['thisRoll'])), 'name'), ' (ID '), e['thisRoll']), ')'))
                if truth(call(get(e['searchTerm'], 'test'), e['item'])):
                    update_env(e, 'count', 1, False)
                    e.set('month', call(get(e['Math'], 'floor'), binary('/', e['day'], 28)))
                    e.set('year', binary('+', 1, call(get(e['Math'], 'floor'), binary('/', e['day'], 112))))
                    e.set('dayOfMonth', binary('%', e['day'], 28))
                    e.set('dayOfWeek', binary('-', binary('%', e['day'], 7), 1))
                    if truth(binary('===', binary('%', e['day'], 112), 0)):
                        e.set('year', binary('-', e['year'], 1))
                    if truth(binary('===', binary('%', e['day'], 28), 0)):
                        e.set('month', binary('-', e['month'], 1))
                        e.set('dayOfMonth', 28)
                    if truth(binary('<', e['dayOfWeek'], 0)):
                        e.set('dayOfWeek', binary('+', e['dayOfWeek'], 7))
                    e.set('monthName', get(get(e['save'], 'seasonNames'), binary('%', e['month'], 4)))
                    e.set('dayOfWeek', get(get(e['save'], 'dayNames'), e['dayOfWeek']))
                    if truth(call(get(e['oasisShirts'], 'includes'), e['numID'])):
                        e.set('extra', '<br/><img src="blank.png" class="icon" id="no_sew"> <span class="note">Oasis exclusive</span>')
                    else:
                        if truth(call(get(e['ccShirts'], 'includes'), e['numID'])):
                            e.set('extra', binary('+', binary('+', '<br/><img src="blank.png" class="icon" id="no_sew"> <span class="note">Character Creator option ', e['spriteID']), '</span>'))
                    e.set('output', binary('+', e['output'], binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', '<tr><td>', e['dayOfWeek']), ' '), e['monthName']), ' '), e['dayOfMonth']), ', Year '), e['year']), '</td><td>'), '<img src="blank.png" class="shirt" id="shirt_'), e['spriteID']), '"></td>'), '<td clas="shirt-name">'), e['item']), e['extra']), '</td>')))
                update_env(e, 'i', 1, False)
            e.set('offset', binary('+', e['offset'], 7))
        e.set('output', binary('+', e['output'], binary('+', binary('+', '<tr><td colspan="3" class="count">Found ', e['count']), ' matching item(s)</td></tr>')))
        e.set('output', binary('+', e['output'], binary('+', binary('+', '<tr><td colspan="3" class="legend">Note: <img src="blank.png" class="icon" id="no_sew" alt="No Sewing"> denotes items which cannot be made via ', call(e['wikify'], 'Tailoring')), '</td></tr>')))
        e.set('output', binary('+', e['output'], '</tbody></table>\n'))
    else:
        if truth((_logic120 if truth(_logic120 := binary('===', unary('typeof', e['offset']), 'undefined')) else binary('===', e['offset'], ''))):
            e.set('offset', binary('*', 7, call(get(e['Math'], 'floor'), binary('/', binary('-', get(e['save'], 'daysPlayed'), 1), 7))))
        call(get(call(e['$'], '#sandy-prev-year'), 'val'), binary('-', e['offset'], 112))
        call(get(call(e['$'], '#sandy-prev-week'), 'val'), binary('-', e['offset'], 7))
        call(get(call(e['$'], '#sandy-next-week'), 'val'), binary('+', e['offset'], 7))
        call(get(call(e['$'], '#sandy-next-year'), 'val'), binary('+', e['offset'], 112))
        if truth(binary('<', e['offset'], 7)):
            call(get(call(e['$'], '#sandy-prev-week'), 'prop'), 'disabled', True)
        else:
            call(get(call(e['$'], '#sandy-prev-week'), 'prop'), 'disabled', False)
        if truth(binary('<', e['offset'], 112)):
            call(get(call(e['$'], '#sandy-prev-year'), 'prop'), 'disabled', True)
        else:
            call(get(call(e['$'], '#sandy-prev-year'), 'prop'), 'disabled', False)
        call(get(call(e['$'], '#sandy-reset'), 'val'), 'reset')
        call(get(call(e['$'], '#sandy-reset'), 'html'), 'Reset Browsing')
        call(get(call(e['$'], '#sandy-next-week'), 'prop'), 'disabled', False)
        call(get(call(e['$'], '#sandy-next-year'), 'prop'), 'disabled', False)
        call(get(call(e['$'], '#sandy-search-text'), 'val'), '')
        call(get(call(e['$'], '#sandy-search-range'), 'val'), 2)
        call(get(call(e['$'], '#sandy-search-all'), 'prop'), 'checked', False)
        e.set('month', call(get(e['Math'], 'floor'), binary('/', e['offset'], 28)))
        e.set('monthName', get(get(e['save'], 'seasonNames'), binary('%', e['month'], 4)))
        e.set('year', binary('+', 1, call(get(e['Math'], 'floor'), binary('/', e['offset'], 112))))
        e.set('dayOfMonth', binary('%', e['offset'], 28))
        e.set('output', binary('+', e['output'], binary('+', '<table class="output"><thead><tr><th class="day">Date</th>', '<th class="shirt-item">Image</th><th class="item">Name</th></tr></thead><tbody>')))
        e.set('dayOfWeek', 1)
        while truth(binary('<', e['dayOfWeek'], 8)):
            e.set('day', binary('+', e['dayOfWeek'], e['offset']))
            e.set('extra', '')
            e.set('numID', 0)
            if truth(binary('>=', call(e['compareSemVer'], get(e['save'], 'version'), '1.6'), 0)):
                e.set('rng', call(e['CSRandom'], call(e['getRandomSeed'], binary('+', e['day'], get(e['save'], 'dayAdjust')), binary('/', get(e['save'], 'gameID'), 2))))
                e.set('result', call(e['getRandomItems'], e['rng'], 'shirts', 1000, 1126, True, True))
                e.set('spriteID', binary('-', get(get(get(e['save'], 'shirts'), get(e['result'], 0)), 'id'), 999))
                e.set('numID', call(e['Number'], get(get(get(e['save'], 'shirts'), get(e['result'], 0)), 'id')))
                e.set('item', binary('+', binary('+', get(get(get(e['save'], 'shirts'), get(e['result'], 0)), 'name'), '<br/>ID: (S)'), get(get(get(e['save'], 'shirts'), get(e['result'], 0)), 'id')))
            else:
                e.set('rng', call(e['CSRandom'], binary('+', binary('+', binary('/', get(e['save'], 'gameID'), 2), e['day']), get(e['save'], 'dayAdjust'))))
                e.set('thisRoll', binary('+', 1000, call(get(e['rng'], 'Next'), 127)))
                e.set('spriteID', binary('-', e['thisRoll'], 999))
                e.set('numID', e['thisRoll'])
                e.set('item', binary('+', binary('+', get(get(get(e['save'], 'shirts'), binary('+', '_', e['thisRoll'])), 'name'), '<br/>ID: '), e['thisRoll']))
            if truth(call(get(e['oasisShirts'], 'includes'), e['numID'])):
                e.set('extra', '<br/><img src="blank.png" class="icon" id="no_sew"> <span class="note">Oasis exclusive</span>')
            else:
                if truth(call(get(e['ccShirts'], 'includes'), e['numID'])):
                    e.set('extra', binary('+', binary('+', '<br/><img src="blank.png" class="icon" id="no_sew"> <span class="note">Character Creator option ', e['spriteID']), '</span>'))
            if truth(binary('<', e['day'], get(e['save'], 'daysPlayed'))):
                e.set('tclass', 'past')
            else:
                if truth(binary('===', e['day'], get(e['save'], 'daysPlayed'))):
                    e.set('tclass', 'current')
                else:
                    e.set('tclass', 'future')
            e.set('output', binary('+', e['output'], binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', '<tr><td class="', e['tclass']), '">'), get(get(e['save'], 'dayNames'), binary('%', binary('-', e['day'], 1), 7))), '<br/>'), e['monthName']), ' '), binary('+', binary('%', binary('-', e['day'], 1), 28), 1)), ', Year '), e['year']), '</td>'), '<td class="'), e['tclass']), '"><img src="blank.png" class="shirt" id="shirt_'), e['spriteID']), '"></td>'), '<td class="'), e['tclass']), ' shirt-name">'), e['item']), e['extra']), '</td></tr>')))
            update_env(e, 'dayOfWeek', 1, False)
        e.set('output', binary('+', e['output'], binary('+', binary('+', '<tr><td colspan="3" class="legend">Note: <img src="blank.png" class="icon" id="no_sew" alt="No Sewing"> denotes items which cannot be made via ', call(e['wikify'], 'Tailoring')), '</td></tr>')))
        e.set('output', binary('+', e['output'], '</tbody></table>\n'))
    return e['output']
    return U


def callback_129(parent, this, args):
    # Upstream predictor: 6085
    e = Env(parent)
    e.declare([])
    e.local['arguments'] = Array(args)
    e.local['key'] = (args[0] if len(args) > 0 and args[0] is not U else U)
    e.local['index'] = (args[1] if len(args) > 1 and args[1] is not U else U)
    e.set('itemIcon', '')
    if truth(unary('!', call(get(get(e['save'], 'donatedItems'), 'hasOwnProperty'), e['key']))):
        e.set('itemIcon', ' <span data-tooltip="Need to Donate"><img src="blank.png" class="icon" id="gunther" alt="Need to Donate"></span>')
    e.set('output', binary('+', e['output'], binary('+', binary('+', binary('+', '<tr><td class="item">', call(e['wikify'], e['key'])), e['itemIcon']), '</td>')))
    e.set('c', 0)
    while truth(binary('<', e['c'], e['numColumns'])):
        if truth(binary('>', get(get(get(e['searchResults'], e['key']), e['c']), 'length'), 0)):
            e.set('output', binary('+', e['output'], binary('+', '<td>', call(get(get(get(e['searchResults'], e['key']), e['c']), 'slice'), 0, 5))))
            if truth(binary('>', get(get(get(e['searchResults'], e['key']), e['c']), 'length'), 5)):
                e.set('output', binary('+', e['output'], binary('+', binary('+', '<span data-tooltip="All results: ', get(get(e['searchResults'], e['key']), e['c'])), '">,...</span>')))
            e.set('output', binary('+', e['output'], '</td>'))
        else:
            e.set('output', binary('+', e['output'], '<td>None</td>'))
        update_env(e, 'c', 1, False)
    e.set('output', binary('+', e['output'], '</tr>'))
    return U


def predictGeodes_121(parent, this, args):
    # Upstream predictor: 5813
    e = Env(parent)
    e.declare(['c', 'couldBeBeans', 'couldBeBeansTrove', 'couldBeHat', 'count', 'g', 'getGoodStuff', 'i', 'item', 'itemID', 'itemIcon', 'itemQty', 'j', 'next', 'numColumns', 'numCracked', 'o', 'output', 'pageSize', 'player', 'prefix', 'prewarm_amount2', 'qty', 'rng', 'rngTrove', 'roll', 'searchEnd', 'searchResults', 'searchStart', 'searchTerm', 'tclass', 'whichPlayer'])
    e.local['arguments'] = Array(args)
    e.local['isSearch'] = (args[0] if len(args) > 0 and args[0] is not U else U)
    e.local['offset'] = (args[1] if len(args) > 1 and args[1] is not U else U)
    e.set('output', '')
    e.set('pageSize', 20)
    e.set('numColumns', 4)
    if truth(binary('>=', call(e['compareSemVer'], get(e['save'], 'version'), '1.4'), 0)):
        update_env(e, 'numColumns', 1, False)
    if truth(binary('>=', call(e['compareSemVer'], get(e['save'], 'version'), '1.5'), 0)):
        update_env(e, 'numColumns', 1, False)
    e.set('whichPlayer', 0)
    if truth((binary('>', get(get(e['save'], 'mp_ids'), 'length'), 1) if truth(_logic122 := binary('!==', unary('typeof', get(e['save'], 'mp_ids')), 'undefined')) else _logic122)):
        call(get(call(e['$'], '#geode-player'), 'show'))
        if truth(binary('==', get(call(e['$'], '#geode-player-select option'), 'length'), 0)):
            e.set('player', 0)
            while truth(binary('<', e['player'], get(get(e['save'], 'mp_ids'), 'length'))):
                e.set('prefix', ('Main Farmer ' if truth(binary('==', e['player'], 0)) else 'Farmhand '))
                e.set('o', call(e['Option'], binary('+', e['prefix'], get(get(e['save'], 'names'), e['player'])), e['player']))
                if truth(binary('==', e['player'], 0)):
                    put(e['o'], 'selected', True)
                call(get(call(e['$'], '#geode-player-select'), 'append'), e['o'])
                update_env(e, 'player', 1, False)
        else:
            e.set('whichPlayer', call(get(call(e['$'], '#geode-player-select'), 'val')))
    else:
        call(get(call(e['$'], '#geode-player'), 'hide'))
    if truth((binary('!==', e['offset'], '') if truth(_logic123 := (binary('!==', unary('typeof', e['offset']), 'undefined') if truth(_logic124 := e['isSearch']) else _logic124)) else _logic123)):
        call(get(call(e['$'], '#geode-prev-100'), 'prop'), 'disabled', True)
        call(get(call(e['$'], '#geode-prev'), 'prop'), 'disabled', True)
        call(get(call(e['$'], '#geode-next'), 'prop'), 'disabled', True)
        call(get(call(e['$'], '#geode-next-100'), 'prop'), 'disabled', True)
        call(get(call(e['$'], '#geode-reset'), 'html'), 'Clear Search Results &amp; Reset Browsing')
        e.set('searchTerm', call(e['RegExp'], e['offset'], 'i'))
        e.set('searchStart', call(get(e['Math'], 'max'), 1, (1 if truth(call(get(call(e['$'], '#geode-search-all'), 'prop'), 'checked')) else get(get(e['save'], 'geodesCracked'), e['whichPlayer']))))
        e.set('searchEnd', binary('+', call(e['parseInt'], call(get(call(e['$'], '#geode-search-range'), 'val'))), e['searchStart']))
        e.set('output', binary('+', e['output'], binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', '<table class="output"><thead><tr><th colspan="', binary('+', e['numColumns'], 2)), '">Search results for &quot;'), e['offset']), '&quot; over the '), ('first ' if truth(call(get(call(e['$'], '#geode-search-all'), 'prop'), 'checked')) else 'next ')), call(get(call(e['$'], '#geode-search-range'), 'val'))), ' geodes</th></tr>\n')))
        e.set('output', binary('+', e['output'], binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', '<tr><th class="item">Item</th>', '<th class="geode-result">Geode <a href="https://stardewvalleywiki.com/Geode">'), '<img src="blank.png" class="icon" id="geode_r"></a></th>'), '<th class="geode-result">Frozen Geode <a href="https://stardewvalleywiki.com/Frozen_Geode">'), '<img src="blank.png" class="icon" id="geode_f"></a></th>'), '<th class="geode-result">Magma Geode <a href="https://stardewvalleywiki.com/Magma_Geode">'), '<img src="blank.png" class="icon" id="geode_m"></a></th>'), '<th class="geode-result">Omni Geode <a href="https://stardewvalleywiki.com/Omni_Geode">'), '<img src="blank.png" class="icon" id="geode_o"></a></th>')))
        if truth(binary('>=', call(e['compareSemVer'], get(e['save'], 'version'), '1.4'), 0)):
            e.set('output', binary('+', e['output'], binary('+', '<th class="geode-result">Artifact Trove <a href="https://stardewvalleywiki.com/Artifact_Trove">', '<img src="blank.png" class="icon" id="geode_t"></a></th>')))
        if truth(binary('>=', call(e['compareSemVer'], get(e['save'], 'version'), '1.5'), 0)):
            e.set('output', binary('+', e['output'], binary('+', '<th class="geode-result">Golden Coconut <a href="https://stardewvalleywiki.com/Golden_Coconut">', '<img src="blank.png" class="icon" id="geode_c"></a></th>')))
        e.set('output', binary('+', e['output'], '</tr>\n<tbody>'))
        e.set('count', 0)
        e.set('searchResults', Obj({}))
        e.set('numCracked', e['searchStart'])
        while truth(binary('<', e['numCracked'], e['searchEnd'])):
            e.set('item', Array(['Stone', 'Stone', 'Stone', 'Stone']))
            e.set('itemQty', Array([1, 1, 1, 1]))
            if truth(binary('>=', call(e['compareSemVer'], get(e['save'], 'version'), '1.6'), 0)):
                if truth(binary('!==', unary('typeof', get(e['save'], 'mp_ids')), 'undefined')):
                    e.set('rng', call(e['CSRandom'], call(e['getRandomSeed'], e['numCracked'], binary('/', get(e['save'], 'gameID'), 2), binary('/', call(e['bigIntToSigned32'], get(get(e['save'], 'mp_ids'), e['whichPlayer'])), 2))))
                    e.set('rngTrove', call(e['CSRandom'], call(e['getRandomSeed'], e['numCracked'], binary('/', get(e['save'], 'gameID'), 2), binary('/', call(e['bigIntToSigned32'], get(get(e['save'], 'mp_ids'), e['whichPlayer'])), 2))))
                else:
                    e.set('rng', call(e['CSRandom'], call(e['getRandomSeed'], e['numCracked'], binary('/', get(e['save'], 'gameID'), 2), 0)))
                    e.set('rngTrove', call(e['CSRandom'], call(e['getRandomSeed'], e['numCracked'], binary('/', get(e['save'], 'gameID'), 2), 0)))
                    call(get(call(e['$'], '#geode-note'), 'html'), 'Note: No players found; predictions will not be reliable for game version >= 1.6')
            else:
                e.set('rng', call(e['CSRandom'], binary('+', e['numCracked'], binary('/', get(e['save'], 'gameID'), 2))))
                e.set('rngTrove', call(e['CSRandom'], binary('+', e['numCracked'], binary('/', get(e['save'], 'gameID'), 2))))
            if truth(binary('>=', call(e['compareSemVer'], get(e['save'], 'version'), '1.4'), 0)):
                e.set('prewarm_amount2', call(get(e['rng'], 'Next'), 1, 10))
                call(get(e['rngTrove'], 'Next'))
                e.set('j', 0)
                while truth(binary('<', e['j'], e['prewarm_amount2'])):
                    call(get(e['rng'], 'NextDouble'))
                    call(get(e['rngTrove'], 'NextDouble'))
                    update_env(e, 'j', 1, False)
                e.set('prewarm_amount2', call(get(e['rng'], 'Next'), 1, 10))
                call(get(e['rngTrove'], 'Next'))
                e.set('i', 0)
                while truth(binary('<', e['i'], e['prewarm_amount2'])):
                    call(get(e['rng'], 'NextDouble'))
                    call(get(e['rngTrove'], 'NextDouble'))
                    update_env(e, 'i', 1, False)
                e.set('couldBeBeans', False)
                e.set('couldBeBeansTrove', False)
                if truth(binary('>=', call(e['compareSemVer'], get(e['save'], 'version'), '1.5'), 0)):
                    e.set('couldBeBeans', binary('<', call(get(e['rng'], 'NextDouble')), 0.1))
                    e.set('couldBeBeansTrove', binary('<', call(get(e['rngTrove'], 'NextDouble')), 0.1))
                e.set('c', call(get(e['rngTrove'], 'NextDouble')))
                call(get(e['item'], 'push'), get(get(get(e['save'], 'objects'), get(get(get(e['save'], 'geodeContents'), 275), call(get(e['Math'], 'floor'), binary('*', e['c'], get(get(get(e['save'], 'geodeContents'), 275), 'length'))))), 'name'))
                call(get(e['itemQty'], 'push'), 1)
                if truth(binary('>=', call(e['compareSemVer'], get(e['save'], 'version'), '1.5'), 0)):
                    e.set('couldBeHat', binary('<', e['c'], 0.05))
                    e.set('roll', call(get(e['Math'], 'floor'), binary('*', e['c'], get(get(get(e['save'], 'geodeContents'), 791), 'length'))))
                    e.set('qty', (5 if truth((_logic125 if truth(_logic125 := (_logic126 if truth(_logic126 := binary('===', e['roll'], 2)) else binary('==', e['roll'], 3))) else binary('==', e['roll'], 6))) else 1))
                    call(get(e['item'], 'push'), get(get(get(e['save'], 'objects'), get(get(get(e['save'], 'geodeContents'), 791), e['roll'])), 'name'))
                    call(get(e['itemQty'], 'push'), e['qty'])
            e.set('getGoodStuff', False)
            e.set('roll', call(get(e['rng'], 'NextDouble')))
            if truth(binary('>=', call(e['compareSemVer'], get(e['save'], 'version'), '1.6'), 0)):
                e.set('getGoodStuff', binary('<', e['roll'], 0.5))
            else:
                e.set('getGoodStuff', unary('!', binary('<', e['roll'], 0.5)))
            if truth(e['getGoodStuff']):
                e.set('next', call(get(e['rng'], 'NextDouble')))
                put(e['item'], 0, get(get(get(e['save'], 'objects'), get(get(get(e['save'], 'geodeContents'), 535), call(get(e['Math'], 'floor'), binary('*', e['next'], get(get(get(e['save'], 'geodeContents'), 535), 'length'))))), 'name'))
                put(e['item'], 1, get(get(get(e['save'], 'objects'), get(get(get(e['save'], 'geodeContents'), 536), call(get(e['Math'], 'floor'), binary('*', e['next'], get(get(get(e['save'], 'geodeContents'), 536), 'length'))))), 'name'))
                put(e['item'], 2, get(get(get(e['save'], 'objects'), get(get(get(e['save'], 'geodeContents'), 537), call(get(e['Math'], 'floor'), binary('*', e['next'], get(get(get(e['save'], 'geodeContents'), 537), 'length'))))), 'name'))
                if truth(binary('>=', call(e['compareSemVer'], get(e['save'], 'version'), '1.6'), 0)):
                    if truth((binary('>', e['numCracked'], 15) if truth(_logic127 := binary('<', e['next'], 0.008)) else _logic127)):
                        put(e['item'], 3, get(get(get(e['save'], 'objects'), '_74'), 'name'))
                    else:
                        put(e['item'], 3, get(get(get(e['save'], 'objects'), get(get(get(e['save'], 'geodeContents'), 749), call(get(e['Math'], 'floor'), call(get(e['rng'], 'Next'), get(get(get(e['save'], 'geodeContents'), 749), 'length'))))), 'name'))
                else:
                    if truth((binary('>', e['numCracked'], 15) if truth(_logic128 := binary('<', call(get(e['rng'], 'NextDouble')), 0.008)) else _logic128)):
                        put(e['item'], 3, get(get(get(e['save'], 'objects'), '_74'), 'name'))
                    else:
                        put(e['item'], 3, get(get(get(e['save'], 'objects'), get(get(get(e['save'], 'geodeContents'), 749), call(get(e['Math'], 'floor'), binary('*', e['next'], get(get(get(e['save'], 'geodeContents'), 749), 'length'))))), 'name'))
            else:
                e.set('qty', binary('+', binary('*', call(get(e['rng'], 'Next'), 3), 2), 1))
                if truth(binary('<', call(get(e['rng'], 'NextDouble')), 0.1)):
                    e.set('qty', 10)
                if truth(binary('<', call(get(e['rng'], 'NextDouble')), 0.01)):
                    e.set('qty', 20)
                if truth(binary('<', call(get(e['rng'], 'NextDouble')), 0.5)):
                    e.set('c', call(get(e['rng'], 'Next'), 4))
                    if truth(binary('<', e['c'], 2)):
                        put(e['item'], 0, get(get(get(e['save'], 'objects'), '_390'), 'name'))
                        put(e['itemQty'], 0, e['qty'])
                        put(e['item'], 1, get(e['item'], 0))
                        put(e['itemQty'], 1, e['qty'])
                        put(e['item'], 2, get(e['item'], 0))
                        put(e['itemQty'], 2, e['qty'])
                        put(e['item'], 3, get(e['item'], 0))
                        put(e['itemQty'], 3, e['qty'])
                    else:
                        if truth(binary('===', e['c'], 2)):
                            put(e['item'], 0, get(get(get(e['save'], 'objects'), '_330'), 'name'))
                            put(e['itemQty'], 0, 1)
                            put(e['item'], 1, get(e['item'], 0))
                            put(e['item'], 2, get(e['item'], 0))
                            put(e['item'], 3, get(e['item'], 0))
                        else:
                            put(e['item'], 0, get(get(get(e['save'], 'objects'), '_86'), 'name'))
                            put(e['itemQty'], 0, 1)
                            put(e['item'], 1, get(get(get(e['save'], 'objects'), '_84'), 'name'))
                            put(e['item'], 2, get(get(get(e['save'], 'objects'), '_82'), 'name'))
                            put(e['item'], 3, get(get(get(e['save'], 'objects'), binary('+', '_', (binary('+', 82, binary('*', call(get(e['rng'], 'Next'), 3), 2)) if truth(binary('>=', call(e['compareSemVer'], get(e['save'], 'version'), '1.3'), 0)) else 82))), 'name'))
                else:
                    e.set('next', call(get(e['rng'], 'NextDouble')))
                    e.set('c', call(get(e['Math'], 'floor'), binary('*', e['next'], 3)))
                    if truth(binary('===', e['c'], 0)):
                        put(e['item'], 0, get(get(get(e['save'], 'objects'), '_378'), 'name'))
                        put(e['itemQty'], 0, e['qty'])
                    else:
                        if truth(binary('===', e['c'], 1)):
                            put(e['item'], 0, get(get(get(e['save'], 'objects'), ('_380' if truth(binary('>', get(e['save'], 'deepestMineLevel'), 25)) else '_378')), 'name'))
                            put(e['itemQty'], 0, e['qty'])
                        else:
                            put(e['item'], 0, get(get(get(e['save'], 'objects'), '_382'), 'name'))
                            put(e['itemQty'], 0, e['qty'])
                    e.set('c', call(get(e['Math'], 'floor'), binary('*', e['next'], 4)))
                    if truth(binary('===', e['c'], 0)):
                        put(e['item'], 1, get(get(get(e['save'], 'objects'), '_378'), 'name'))
                        put(e['itemQty'], 1, e['qty'])
                    else:
                        if truth(binary('===', e['c'], 1)):
                            put(e['item'], 1, get(get(get(e['save'], 'objects'), '_380'), 'name'))
                            put(e['itemQty'], 1, e['qty'])
                        else:
                            if truth(binary('===', e['c'], 2)):
                                put(e['item'], 1, get(get(get(e['save'], 'objects'), '_382'), 'name'))
                                put(e['itemQty'], 1, e['qty'])
                            else:
                                put(e['item'], 1, get(get(get(e['save'], 'objects'), ('_384' if truth(binary('>', get(e['save'], 'deepestMineLevel'), 75)) else '_380')), 'name'))
                                put(e['itemQty'], 1, e['qty'])
                    e.set('c', call(get(e['Math'], 'floor'), binary('*', e['next'], 5)))
                    if truth(binary('===', e['c'], 0)):
                        put(e['item'], 2, get(get(get(e['save'], 'objects'), '_378'), 'name'))
                        put(e['item'], 3, get(e['item'], 2))
                        put(e['itemQty'], 2, e['qty'])
                        put(e['itemQty'], 3, get(e['itemQty'], 2))
                    else:
                        if truth(binary('===', e['c'], 1)):
                            put(e['item'], 2, get(get(get(e['save'], 'objects'), '_380'), 'name'))
                            put(e['item'], 3, get(e['item'], 2))
                            put(e['itemQty'], 2, e['qty'])
                            put(e['itemQty'], 3, get(e['itemQty'], 2))
                        else:
                            if truth(binary('===', e['c'], 2)):
                                put(e['item'], 2, get(get(get(e['save'], 'objects'), '_382'), 'name'))
                                put(e['item'], 3, get(e['item'], 2))
                                put(e['itemQty'], 2, e['qty'])
                                put(e['itemQty'], 3, get(e['itemQty'], 2))
                            else:
                                if truth(binary('===', e['c'], 3)):
                                    put(e['item'], 2, get(get(get(e['save'], 'objects'), '_384'), 'name'))
                                    put(e['item'], 3, get(e['item'], 2))
                                    put(e['itemQty'], 2, e['qty'])
                                    put(e['itemQty'], 3, get(e['itemQty'], 2))
                                else:
                                    put(e['item'], 2, get(get(get(e['save'], 'objects'), '_386'), 'name'))
                                    put(e['item'], 3, get(e['item'], 2))
                                    put(e['itemQty'], 2, call(get(e['Math'], 'floor'), binary('+', binary('/', e['qty'], 2), 1)))
                                    put(e['itemQty'], 3, get(e['itemQty'], 2))
            e.set('c', 0)
            while truth(binary('<', e['c'], e['numColumns'])):
                if truth(call(get(e['searchTerm'], 'test'), get(e['item'], e['c']))):
                    if truth(unary('!', call(get(e['searchResults'], 'hasOwnProperty'), get(e['item'], e['c'])))):
                        put(e['searchResults'], get(e['item'], e['c']), Array([Array([]), Array([]), Array([]), Array([])]))
                        if truth(binary('>=', call(e['compareSemVer'], get(e['save'], 'version'), '1.4'), 0)):
                            call(get(get(e['searchResults'], get(e['item'], e['c'])), 'push'), Array([]))
                        if truth(binary('>=', call(e['compareSemVer'], get(e['save'], 'version'), '1.5'), 0)):
                            call(get(get(e['searchResults'], get(e['item'], e['c'])), 'push'), Array([]))
                    call(get(get(get(e['searchResults'], get(e['item'], e['c'])), e['c']), 'push'), e['numCracked'])
                    update_env(e, 'count', 1, False)
                update_env(e, 'c', 1, False)
            update_env(e, 'numCracked', 1, False)
        call(get(call(get(call(get(e['Object'], 'keys'), e['searchResults']), 'sort')), 'forEach'), Fn(callback_129, e))
        e.set('output', binary('+', e['output'], binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', '<tr><td colspan="', binary('+', e['numColumns'], 1)), '" class="count">Found '), e['count']), ' matching instance(s) of '), get(call(get(e['Object'], 'keys'), e['searchResults']), 'length')), ' matching item(s)</td></tr>\n')))
    else:
        if truth(binary('===', unary('typeof', e['offset']), 'undefined')):
            e.set('offset', binary('*', e['pageSize'], call(get(e['Math'], 'floor'), binary('/', get(get(e['save'], 'geodesCracked'), e['whichPlayer']), e['pageSize']))))
        if truth(binary('<', e['offset'], e['pageSize'])):
            call(get(call(e['$'], '#geode-prev'), 'prop'), 'disabled', True)
        else:
            call(get(call(e['$'], '#geode-prev'), 'val'), binary('-', e['offset'], e['pageSize']))
            call(get(call(e['$'], '#geode-prev'), 'prop'), 'disabled', False)
        if truth(binary('<', e['offset'], 100)):
            call(get(call(e['$'], '#geode-prev-100'), 'prop'), 'disabled', True)
        else:
            call(get(call(e['$'], '#geode-prev-100'), 'val'), binary('-', e['offset'], 100))
            call(get(call(e['$'], '#geode-prev-100'), 'prop'), 'disabled', False)
        call(get(call(e['$'], '#geode-reset'), 'val'), 'reset')
        call(get(call(e['$'], '#geode-reset'), 'html'), 'Reset Browsing')
        call(get(call(e['$'], '#geode-next'), 'val'), binary('+', e['offset'], e['pageSize']))
        call(get(call(e['$'], '#geode-next'), 'prop'), 'disabled', False)
        call(get(call(e['$'], '#geode-next-100'), 'val'), binary('+', e['offset'], 100))
        call(get(call(e['$'], '#geode-next-100'), 'prop'), 'disabled', False)
        call(get(call(e['$'], '#geode-search-text'), 'val'), '')
        call(get(call(e['$'], '#geode-search-range'), 'val'), 200)
        call(get(call(e['$'], '#geode-search-all'), 'prop'), 'checked', False)
        e.set('output', binary('+', e['output'], binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', '<table class="output"><thead><tr><th rowspan="2" class="index">Num Open</th>', '<th colspan="2" class="multi">Geode <a href="https://stardewvalleywiki.com/Geode">'), '<img src="blank.png" class="icon" id="geode_r"></a></th>'), '<th colspan="2" class="multi">Frozen Geode <a href="https://stardewvalleywiki.com/Frozen_Geode">'), '<img src="blank.png" class="icon" id="geode_f"></a></th>'), '<th colspan="2" class="multi">Magma Geode <a href="https://stardewvalleywiki.com/Magma_Geode">'), '<img src="blank.png" class="icon" id="geode_m"></a></th>'), '<th colspan="2" class="multi">Omni Geode <a href="https://stardewvalleywiki.com/Omni_Geode">'), '<img src="blank.png" class="icon" id="geode_o"></a></th>')))
        if truth(binary('>=', call(e['compareSemVer'], get(e['save'], 'version'), '1.4'), 0)):
            e.set('output', binary('+', e['output'], binary('+', '<th colspan="2" class="multi"">Artifact Trove <a href="https://stardewvalleywiki.com/Artifact_Trove">', '<img src="blank.png" class="icon" id="geode_t"></a></th>')))
        if truth(binary('>=', call(e['compareSemVer'], get(e['save'], 'version'), '1.5'), 0)):
            e.set('output', binary('+', e['output'], binary('+', '<th colspan="2" class="multi"">Golden Coconut <a href="https://stardewvalleywiki.com/Golden_Coconut">', '<img src="blank.png" class="icon" id="geode_c"></a></th>')))
        e.set('output', binary('+', e['output'], '</tr>\n<tr>'))
        e.set('c', 0)
        while truth(binary('<', e['c'], e['numColumns'])):
            e.set('output', binary('+', e['output'], '<th class="item">Item</th><th class="qty">Qty</th>'))
            update_env(e, 'c', 1, False)
        e.set('output', binary('+', e['output'], '</tr>\n<tbody>'))
        e.set('g', 1)
        while truth(binary('<=', e['g'], e['pageSize'])):
            e.set('numCracked', binary('+', e['offset'], e['g']))
            e.set('couldBeHat', False)
            e.set('item', Array(['Stone', 'Stone', 'Stone', 'Stone']))
            e.set('itemQty', Array([1, 1, 1, 1]))
            if truth(binary('>=', call(e['compareSemVer'], get(e['save'], 'version'), '1.6'), 0)):
                if truth(binary('!==', unary('typeof', get(e['save'], 'mp_ids')), 'undefined')):
                    e.set('rng', call(e['CSRandom'], call(e['getRandomSeed'], e['numCracked'], binary('/', get(e['save'], 'gameID'), 2), binary('/', call(e['bigIntToSigned32'], get(get(e['save'], 'mp_ids'), e['whichPlayer'])), 2))))
                    e.set('rngTrove', call(e['CSRandom'], call(e['getRandomSeed'], e['numCracked'], binary('/', get(e['save'], 'gameID'), 2), binary('/', call(e['bigIntToSigned32'], get(get(e['save'], 'mp_ids'), e['whichPlayer'])), 2))))
                else:
                    e.set('rng', call(e['CSRandom'], call(e['getRandomSeed'], e['numCracked'], binary('/', get(e['save'], 'gameID'), 2), 0)))
                    e.set('rngTrove', call(e['CSRandom'], call(e['getRandomSeed'], e['numCracked'], binary('/', get(e['save'], 'gameID'), 2), 0)))
                    call(get(call(e['$'], '#geode-note'), 'html'), 'Note: No players found; predictions will not be reliable for game version >= 1.6')
            else:
                e.set('rng', call(e['CSRandom'], binary('+', e['numCracked'], binary('/', get(e['save'], 'gameID'), 2))))
                e.set('rngTrove', call(e['CSRandom'], binary('+', e['numCracked'], binary('/', get(e['save'], 'gameID'), 2))))
            if truth(binary('>=', call(e['compareSemVer'], get(e['save'], 'version'), '1.4'), 0)):
                e.set('prewarm_amount2', call(get(e['rng'], 'Next'), 1, 10))
                call(get(e['rngTrove'], 'Next'))
                e.set('j', 0)
                while truth(binary('<', e['j'], e['prewarm_amount2'])):
                    call(get(e['rng'], 'NextDouble'))
                    call(get(e['rngTrove'], 'NextDouble'))
                    update_env(e, 'j', 1, False)
                e.set('prewarm_amount2', call(get(e['rng'], 'Next'), 1, 10))
                call(get(e['rngTrove'], 'Next'))
                e.set('i', 0)
                while truth(binary('<', e['i'], e['prewarm_amount2'])):
                    call(get(e['rng'], 'NextDouble'))
                    call(get(e['rngTrove'], 'NextDouble'))
                    update_env(e, 'i', 1, False)
                e.set('couldBeBeans', False)
                e.set('couldBeBeansTrove', False)
                if truth(binary('>=', call(e['compareSemVer'], get(e['save'], 'version'), '1.5'), 0)):
                    e.set('couldBeBeans', binary('<', call(get(e['rng'], 'NextDouble')), 0.1))
                    e.set('couldBeBeansTrove', binary('<', call(get(e['rngTrove'], 'NextDouble')), 0.1))
                e.set('c', call(get(e['rngTrove'], 'NextDouble')))
                call(get(e['item'], 'push'), get(get(get(e['save'], 'objects'), get(get(get(e['save'], 'geodeContents'), 275), call(get(e['Math'], 'floor'), binary('*', e['c'], get(get(get(e['save'], 'geodeContents'), 275), 'length'))))), 'name'))
                call(get(e['itemQty'], 'push'), 1)
                if truth(binary('>=', call(e['compareSemVer'], get(e['save'], 'version'), '1.5'), 0)):
                    e.set('couldBeHat', binary('<', e['c'], 0.05))
                    e.set('roll', call(get(e['Math'], 'floor'), binary('*', call(get(e['rngTrove'], 'NextDouble')), get(get(get(e['save'], 'geodeContents'), 791), 'length'))))
                    e.set('qty', (5 if truth((_logic130 if truth(_logic130 := (_logic131 if truth(_logic131 := binary('===', e['roll'], 2)) else binary('==', e['roll'], 3))) else binary('==', e['roll'], 6))) else 1))
                    call(get(e['item'], 'push'), get(get(get(e['save'], 'objects'), get(get(get(e['save'], 'geodeContents'), 791), e['roll'])), 'name'))
                    call(get(e['itemQty'], 'push'), e['qty'])
            e.set('getGoodStuff', False)
            e.set('roll', call(get(e['rng'], 'NextDouble')))
            if truth(binary('>=', call(e['compareSemVer'], get(e['save'], 'version'), '1.6'), 0)):
                e.set('getGoodStuff', binary('<', e['roll'], 0.5))
            else:
                e.set('getGoodStuff', unary('!', binary('<', e['roll'], 0.5)))
            if truth(e['getGoodStuff']):
                e.set('next', call(get(e['rng'], 'NextDouble')))
                put(e['item'], 0, get(get(get(e['save'], 'objects'), get(get(get(e['save'], 'geodeContents'), 535), call(get(e['Math'], 'floor'), binary('*', e['next'], get(get(get(e['save'], 'geodeContents'), 535), 'length'))))), 'name'))
                put(e['item'], 1, get(get(get(e['save'], 'objects'), get(get(get(e['save'], 'geodeContents'), 536), call(get(e['Math'], 'floor'), binary('*', e['next'], get(get(get(e['save'], 'geodeContents'), 536), 'length'))))), 'name'))
                put(e['item'], 2, get(get(get(e['save'], 'objects'), get(get(get(e['save'], 'geodeContents'), 537), call(get(e['Math'], 'floor'), binary('*', e['next'], get(get(get(e['save'], 'geodeContents'), 537), 'length'))))), 'name'))
                if truth(binary('>=', call(e['compareSemVer'], get(e['save'], 'version'), '1.6'), 0)):
                    if truth((binary('>', e['numCracked'], 15) if truth(_logic132 := binary('<', e['next'], 0.008)) else _logic132)):
                        put(e['item'], 3, get(get(get(e['save'], 'objects'), '_74'), 'name'))
                    else:
                        put(e['item'], 3, get(get(get(e['save'], 'objects'), get(get(get(e['save'], 'geodeContents'), 749), call(get(e['Math'], 'floor'), call(get(e['rng'], 'Next'), get(get(get(e['save'], 'geodeContents'), 749), 'length'))))), 'name'))
                else:
                    if truth((binary('>', e['numCracked'], 15) if truth(_logic133 := binary('<', call(get(e['rng'], 'NextDouble')), 0.008)) else _logic133)):
                        put(e['item'], 3, get(get(get(e['save'], 'objects'), '_74'), 'name'))
                    else:
                        put(e['item'], 3, get(get(get(e['save'], 'objects'), get(get(get(e['save'], 'geodeContents'), 749), call(get(e['Math'], 'floor'), binary('*', e['next'], get(get(get(e['save'], 'geodeContents'), 749), 'length'))))), 'name'))
            else:
                e.set('qty', binary('+', binary('*', call(get(e['rng'], 'Next'), 3), 2), 1))
                if truth(binary('<', call(get(e['rng'], 'NextDouble')), 0.1)):
                    e.set('qty', 10)
                if truth(binary('<', call(get(e['rng'], 'NextDouble')), 0.01)):
                    e.set('qty', 20)
                if truth(binary('<', call(get(e['rng'], 'NextDouble')), 0.5)):
                    e.set('c', call(get(e['rng'], 'Next'), 4))
                    if truth(binary('<', e['c'], 2)):
                        put(e['item'], 0, get(get(get(e['save'], 'objects'), '_390'), 'name'))
                        put(e['itemQty'], 0, e['qty'])
                        put(e['item'], 1, get(e['item'], 0))
                        put(e['itemQty'], 1, e['qty'])
                        put(e['item'], 2, get(e['item'], 0))
                        put(e['itemQty'], 2, e['qty'])
                        put(e['item'], 3, get(e['item'], 0))
                        put(e['itemQty'], 3, e['qty'])
                    else:
                        if truth(binary('===', e['c'], 2)):
                            put(e['item'], 0, get(get(get(e['save'], 'objects'), '_330'), 'name'))
                            put(e['itemQty'], 0, 1)
                            put(e['item'], 1, get(e['item'], 0))
                            put(e['item'], 2, get(e['item'], 0))
                            put(e['item'], 3, get(e['item'], 0))
                        else:
                            put(e['item'], 0, get(get(get(e['save'], 'objects'), '_86'), 'name'))
                            put(e['itemQty'], 0, 1)
                            put(e['item'], 1, get(get(get(e['save'], 'objects'), '_84'), 'name'))
                            put(e['item'], 2, get(get(get(e['save'], 'objects'), '_82'), 'name'))
                            put(e['item'], 3, get(get(get(e['save'], 'objects'), binary('+', '_', (binary('+', 82, binary('*', call(get(e['rng'], 'Next'), 3), 2)) if truth(binary('>=', call(e['compareSemVer'], get(e['save'], 'version'), '1.3'), 0)) else 82))), 'name'))
                else:
                    e.set('next', call(get(e['rng'], 'NextDouble')))
                    e.set('c', call(get(e['Math'], 'floor'), binary('*', e['next'], 3)))
                    if truth(binary('===', e['c'], 0)):
                        put(e['item'], 0, get(get(get(e['save'], 'objects'), '_378'), 'name'))
                        put(e['itemQty'], 0, e['qty'])
                    else:
                        if truth(binary('===', e['c'], 1)):
                            put(e['item'], 0, get(get(get(e['save'], 'objects'), ('_380' if truth(binary('>', get(e['save'], 'deepestMineLevel'), 25)) else '_378')), 'name'))
                            put(e['itemQty'], 0, e['qty'])
                        else:
                            put(e['item'], 0, get(get(get(e['save'], 'objects'), '_382'), 'name'))
                            put(e['itemQty'], 0, e['qty'])
                    e.set('c', call(get(e['Math'], 'floor'), binary('*', e['next'], 4)))
                    if truth(binary('===', e['c'], 0)):
                        put(e['item'], 1, get(get(get(e['save'], 'objects'), '_378'), 'name'))
                        put(e['itemQty'], 1, e['qty'])
                    else:
                        if truth(binary('===', e['c'], 1)):
                            put(e['item'], 1, get(get(get(e['save'], 'objects'), '_380'), 'name'))
                            put(e['itemQty'], 1, e['qty'])
                        else:
                            if truth(binary('===', e['c'], 2)):
                                put(e['item'], 1, get(get(get(e['save'], 'objects'), '_382'), 'name'))
                                put(e['itemQty'], 1, e['qty'])
                            else:
                                put(e['item'], 1, get(get(get(e['save'], 'objects'), ('_384' if truth(binary('>', get(e['save'], 'deepestMineLevel'), 75)) else '_380')), 'name'))
                                put(e['itemQty'], 1, e['qty'])
                    e.set('c', call(get(e['Math'], 'floor'), binary('*', e['next'], 5)))
                    if truth(binary('===', e['c'], 0)):
                        put(e['item'], 2, get(get(get(e['save'], 'objects'), '_378'), 'name'))
                        put(e['item'], 3, get(e['item'], 2))
                        put(e['itemQty'], 2, e['qty'])
                        put(e['itemQty'], 3, get(e['itemQty'], 2))
                    else:
                        if truth(binary('===', e['c'], 1)):
                            put(e['item'], 2, get(get(get(e['save'], 'objects'), '_380'), 'name'))
                            put(e['item'], 3, get(e['item'], 2))
                            put(e['itemQty'], 2, e['qty'])
                            put(e['itemQty'], 3, get(e['itemQty'], 2))
                        else:
                            if truth(binary('===', e['c'], 2)):
                                put(e['item'], 2, get(get(get(e['save'], 'objects'), '_382'), 'name'))
                                put(e['item'], 3, get(e['item'], 2))
                                put(e['itemQty'], 2, e['qty'])
                                put(e['itemQty'], 3, get(e['itemQty'], 2))
                            else:
                                if truth(binary('===', e['c'], 3)):
                                    put(e['item'], 2, get(get(get(e['save'], 'objects'), '_384'), 'name'))
                                    put(e['item'], 3, get(e['item'], 2))
                                    put(e['itemQty'], 2, e['qty'])
                                    put(e['itemQty'], 3, get(e['itemQty'], 2))
                                else:
                                    put(e['item'], 2, get(get(get(e['save'], 'objects'), '_386'), 'name'))
                                    put(e['item'], 3, get(e['item'], 2))
                                    put(e['itemQty'], 2, call(get(e['Math'], 'floor'), binary('+', binary('/', e['qty'], 2), 1)))
                                    put(e['itemQty'], 3, get(e['itemQty'], 2))
            if truth(binary('===', e['numCracked'], binary('+', get(get(e['save'], 'geodesCracked'), e['whichPlayer']), 1))):
                e.set('tclass', 'current')
            else:
                if truth(binary('<=', e['numCracked'], get(get(e['save'], 'geodesCracked'), e['whichPlayer']))):
                    e.set('tclass', 'past')
                else:
                    e.set('tclass', 'future')
            e.set('output', binary('+', e['output'], binary('+', binary('+', binary('+', binary('+', '<tr class="', e['tclass']), '"><td>'), call(e['addCommas'], e['numCracked'])), '</td>')))
            e.set('c', 0)
            while truth(binary('<', e['c'], e['numColumns'])):
                e.set('itemIcon', '')
                if truth(binary('===', e['c'], 5)):
                    if truth(e['couldBeHat']):
                        e.set('itemIcon', ' <span data-tooltip="Could be Golden Helmet"><img src="blank.png" class="icon" id="icon_h" alt="Could be Golden Helmet"></span>')
                    if truth(e['couldBeBeansTrove']):
                        e.set('itemIcon', binary('+', e['itemIcon'], ' <span data-tooltip="Could be Qi Beans"><img src="blank.png" class="icon" id="icon_b" alt="Could be Qi Beans"></span>'))
                else:
                    if truth(unary('!', call(get(get(e['save'], 'donatedItems'), 'hasOwnProperty'), get(e['item'], e['c'])))):
                        e.set('itemIcon', ' <span data-tooltip="Need to Donate"><img src="blank.png" class="icon" id="gunther" alt="Need to Donate"></span>')
                    if truth(binary('===', e['c'], 4)):
                        if truth(e['couldBeBeansTrove']):
                            e.set('itemIcon', binary('+', e['itemIcon'], ' <span data-tooltip="Could be Qi Beans"><img src="blank.png" class="icon" id="icon_b" alt="Could be Qi Beans"></span>'))
                    else:
                        if truth(e['couldBeBeans']):
                            e.set('itemIcon', binary('+', e['itemIcon'], ' <span data-tooltip="Could be Qi Beans"><img src="blank.png" class="icon" id="icon_b" alt="Could be Qi Beans"></span>'))
                e.set('output', binary('+', e['output'], binary('+', binary('+', binary('+', binary('+', binary('+', '<td class="item">', call(e['wikify'], get(e['item'], e['c']))), e['itemIcon']), '</td><td>'), get(e['itemQty'], e['c'])), '</td>')))
                update_env(e, 'c', 1, False)
            e.set('output', binary('+', e['output'], '</tr>'))
            update_env(e, 'g', 1, False)
    e.set('output', binary('+', e['output'], binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', '<tr><td colspan="', binary('+', 1, binary('*', 2, e['numColumns']))), '" class="legend">Note: <img src="blank.png" class="icon" id="gunther" alt="Need to Donate"> denotes items '), 'which need to be donated to the '), call(e['wikify'], 'Museum')), '<br/> <img src="blank.png" class="icon" id="icon_b" alt="Could be Qi Beans"> denotes items which will be replaced by '), call(e['wikify'], 'Qi Beans')), ' and <img src="blank.png" class="icon" id="icon_h" alt="Could be Golden Coconut Hat"> denotes items which will be replaced by the '), call(e['wikify'], 'Golden Helmet')), ' if applicable.</td></tr>')))
    e.set('output', binary('+', e['output'], '</tbody></table>'))
    return e['output']
    return U


def callback_145(parent, this, args):
    # Upstream predictor: 6648
    e = Env(parent)
    e.declare([])
    e.local['arguments'] = Array(args)
    e.local['key'] = (args[0] if len(args) > 0 and args[0] is not U else U)
    e.local['index'] = (args[1] if len(args) > 1 and args[1] is not U else U)
    e.set('itemIcon', (' <span data-tooltip="Based on Fishing Skill"><img src="blank.png" class="icon" id="enchant_f" alt="Based on Fishing Skill"></span>' if truth((_logic146 if truth(_logic146 := binary('==', e['key'], 'Cork Bobber')) else binary('==', e['key'], 'Dressed Spinner'))) else ''))
    e.set('output', binary('+', e['output'], binary('+', binary('+', binary('+', '<tr><td class="item">', call(e['wikify'], e['key'])), e['itemIcon']), '</td>')))
    e.set('c', 0)
    while truth(binary('<', e['c'], e['numColumns'])):
        if truth(binary('>', get(get(get(e['searchResults'], e['key']), e['c']), 'length'), 0)):
            e.set('output', binary('+', e['output'], binary('+', '<td>', call(get(get(get(e['searchResults'], e['key']), e['c']), 'slice'), 0, 5))))
            if truth(binary('>', get(get(get(e['searchResults'], e['key']), e['c']), 'length'), 5)):
                e.set('output', binary('+', e['output'], binary('+', binary('+', '<span data-tooltip="All results: ', get(get(e['searchResults'], e['key']), e['c'])), '">,...</span>')))
            e.set('output', binary('+', e['output'], '</td>'))
        else:
            e.set('output', binary('+', e['output'], '<td>None</td>'))
        update_env(e, 'c', 1, False)
    e.set('output', binary('+', e['output'], '</tr>'))
    return U


def predictMysteryBoxes_134(parent, this, args):
    # Upstream predictor: 6368
    e = Env(parent)
    e.declare(['basedOnSkill', 'c', 'choices', 'count', 'extraBookChance', 'g', 'i', 'item', 'itemIcon', 'itemQty', 'j', 'next', 'noLink', 'numColumns', 'numOpened', 'o', 'output', 'pageSize', 'player', 'prefix', 'prewarm_amount2', 'qty', 'rareMod', 'rng', 'roll', 'searchEnd', 'searchResults', 'searchStart', 'searchTerm', 'tclass', 'whichPlayer'])
    e.local['arguments'] = Array(args)
    e.local['isSearch'] = (args[0] if len(args) > 0 and args[0] is not U else U)
    e.local['offset'] = (args[1] if len(args) > 1 and args[1] is not U else U)
    e.set('output', '')
    e.set('pageSize', 20)
    e.set('numColumns', 3)
    e.set('whichPlayer', 0)
    if truth((binary('>', get(get(e['save'], 'mp_ids'), 'length'), 1) if truth(_logic135 := binary('!==', unary('typeof', get(e['save'], 'mp_ids')), 'undefined')) else _logic135)):
        call(get(call(e['$'], '#mystery-player'), 'show'))
        if truth(binary('==', get(call(e['$'], '#mystery-player-select option'), 'length'), 0)):
            e.set('player', 0)
            while truth(binary('<', e['player'], get(get(e['save'], 'mp_ids'), 'length'))):
                e.set('prefix', ('Main Farmer ' if truth(binary('==', e['player'], 0)) else 'Farmhand '))
                e.set('o', call(e['Option'], binary('+', e['prefix'], get(get(e['save'], 'names'), e['player'])), e['player']))
                if truth(binary('==', e['player'], 0)):
                    put(e['o'], 'selected', True)
                call(get(call(e['$'], '#mystery-player-select'), 'append'), e['o'])
                update_env(e, 'player', 1, False)
        else:
            e.set('whichPlayer', call(get(call(e['$'], '#mystery-player-select'), 'val')))
    else:
        call(get(call(e['$'], '#mystery-player'), 'hide'))
    if truth((binary('!==', e['offset'], '') if truth(_logic136 := (binary('!==', unary('typeof', e['offset']), 'undefined') if truth(_logic137 := e['isSearch']) else _logic137)) else _logic136)):
        call(get(call(e['$'], '#mystery-prev-100'), 'prop'), 'disabled', True)
        call(get(call(e['$'], '#mystery-prev'), 'prop'), 'disabled', True)
        call(get(call(e['$'], '#mystery-next'), 'prop'), 'disabled', True)
        call(get(call(e['$'], '#mystery-next-100'), 'prop'), 'disabled', True)
        call(get(call(e['$'], '#mystery-reset'), 'html'), 'Clear Search Results &amp; Reset Browsing')
        e.set('searchTerm', call(e['RegExp'], e['offset'], 'i'))
        e.set('searchStart', call(get(e['Math'], 'max'), 1, (1 if truth(call(get(call(e['$'], '#mystery-search-all'), 'prop'), 'checked')) else get(get(e['save'], 'mysteryBoxesOpened'), e['whichPlayer']))))
        e.set('searchEnd', binary('+', call(e['parseInt'], call(get(call(e['$'], '#mystery-search-range'), 'val'))), e['searchStart']))
        e.set('output', binary('+', e['output'], binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', '<table class="output"><thead><tr><th colspan="', binary('+', e['numColumns'], 2)), '">Search results for &quot;'), e['offset']), '&quot; over the '), ('first ' if truth(call(get(call(e['$'], '#mystery-search-all'), 'prop'), 'checked')) else 'next ')), call(get(call(e['$'], '#mystery-search-range'), 'val'))), ' mystery boxes</th></tr>\n')))
        e.set('output', binary('+', e['output'], binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', '<tr><th class="item">Item</th>', '<th class="mystery-result">Mystery Box <a href="https://stardewvalleywiki.com/Mystery_Box">'), '<img src="blank.png" class="icon" id="mbox_b"></a></th>'), '<th class="mystery-result">Golden Mystery Box <a href="https://stardewvalleywiki.com/Golden_Mystery_Box">'), '<img src="blank.png" class="icon" id="mbox_g"></a><br/>Without Farming Mastery Perk</th>'), '<th class="mystery-result">Golden Mystery Box <a href="https://stardewvalleywiki.com/Golden_Mystery_Box">'), '<img src="blank.png" class="icon" id="mbox_g"></a><br/>With Farming Mastery Perk</th>')))
        e.set('output', binary('+', e['output'], '</tr>\n<tbody>'))
        e.set('count', 0)
        e.set('searchResults', Obj({}))
        e.set('numOpened', e['searchStart'])
        while truth(binary('<', e['numOpened'], e['searchEnd'])):
            e.set('item', Array(['None', 'None', 'None']))
            e.set('itemQty', Array([1, 1, 1]))
            e.set('noLink', Array([False, False, False]))
            e.set('basedOnSkill', Array([False, False, False]))
            e.set('c', 0)
            while truth(binary('<', e['c'], e['numColumns'])):
                e.set('rareMod', (1 if truth(binary('===', e['c'], 0)) else 2))
                e.set('extraBookChance', (0 if truth(get(e['save'], 'gotMysteryBook')) else binary('*', 0.0004, e['numOpened'])))
                if truth(binary('!==', unary('typeof', get(e['save'], 'mp_ids')), 'undefined')):
                    e.set('rng', call(e['CSRandom'], call(e['getRandomSeed'], e['numOpened'], binary('/', get(e['save'], 'gameID'), 2), binary('/', call(e['bigIntToSigned32'], get(get(e['save'], 'mp_ids'), e['whichPlayer'])), 2))))
                else:
                    e.set('rng', call(e['CSRandom'], call(e['getRandomSeed'], e['numOpened'], binary('/', get(e['save'], 'gameID'), 2), 0)))
                    call(get(call(e['$'], '#mystery-note'), 'html'), 'Note: No players found; predictions will not be reliable for game version >= 1.6')
                e.set('prewarm_amount2', call(get(e['rng'], 'Next'), 1, 10))
                e.set('j', 0)
                while truth(binary('<', e['j'], e['prewarm_amount2'])):
                    call(get(e['rng'], 'NextDouble'))
                    update_env(e, 'j', 1, False)
                e.set('prewarm_amount2', call(get(e['rng'], 'Next'), 1, 10))
                e.set('i', 0)
                while truth(binary('<', e['i'], e['prewarm_amount2'])):
                    call(get(e['rng'], 'NextDouble'))
                    update_env(e, 'i', 1, False)
                if truth((_logic138 if truth(_logic138 := binary('>', e['numOpened'], 10)) else binary('>', e['c'], 0))):
                    if truth((binary('<', call(get(e['rng'], 'NextDouble')), 0.005) if truth(_logic139 := binary('==', e['c'], 2)) else _logic139)):
                        put(e['item'], e['c'], 'Golden Animal Cracker')
                    else:
                        if truth((binary('<', call(get(e['rng'], 'NextDouble')), 0.005) if truth(_logic140 := binary('>', e['c'], 0)) else _logic140)):
                            put(e['item'], e['c'], 'Auto-Petter')
                        else:
                            if truth(binary('<', call(get(e['rng'], 'NextDouble')), binary('*', 0.002, e['rareMod']))):
                                put(e['item'], e['c'], get(get(get(e['save'], 'objects'), '_279'), 'name'))
                            else:
                                if truth(binary('<', call(get(e['rng'], 'NextDouble')), binary('*', 0.004, e['rareMod']))):
                                    put(e['item'], e['c'], get(get(get(e['save'], 'objects'), '_74'), 'name'))
                                else:
                                    if truth(binary('<', call(get(e['rng'], 'NextDouble')), binary('*', 0.008, e['rareMod']))):
                                        put(e['item'], e['c'], get(get(get(e['save'], 'objects'), '_166'), 'name'))
                                    else:
                                        if truth(binary('<', call(get(e['rng'], 'NextDouble')), binary('+', binary('*', 0.01, e['rareMod']), e['extraBookChance']))):
                                            if truth(unary('!', get(e['save'], 'gotMysteryBook'))):
                                                put(e['item'], e['c'], get(get(get(e['save'], 'objects'), '_Book_Mystery'), 'name'))
                                            else:
                                                e.set('choices', Array(['_PurpleBook', '_Book_Mystery']))
                                                put(e['item'], e['c'], get(get(get(e['save'], 'objects'), get(e['choices'], call(get(e['rng'], 'Next'), get(e['choices'], 'length')))), 'name'))
                                        else:
                                            if truth(binary('<', call(get(e['rng'], 'NextDouble')), binary('*', 0.01, e['rareMod']))):
                                                e.set('choices', Array(['_797', '_373']))
                                                put(e['item'], e['c'], get(get(get(e['save'], 'objects'), get(e['choices'], call(get(e['rng'], 'Next'), get(e['choices'], 'length')))), 'name'))
                                            else:
                                                if truth(binary('<', call(get(e['rng'], 'NextDouble')), binary('*', 0.01, e['rareMod']))):
                                                    put(e['item'], e['c'], 'Mystery Hat')
                                                else:
                                                    if truth(binary('<', call(get(e['rng'], 'NextDouble')), binary('*', 0.01, e['rareMod']))):
                                                        put(e['item'], e['c'], 'Mystery Shirt')
                                                    else:
                                                        if truth(binary('<', call(get(e['rng'], 'NextDouble')), binary('*', 0.01, e['rareMod']))):
                                                            put(e['item'], e['c'], 'Mystery Wallpaper')
                                                        else:
                                                            if truth((_logic141 if truth(_logic141 := binary('<', call(get(e['rng'], 'NextDouble')), 0.1)) else binary('>', e['c'], 0))):
                                                                _switch142 = call(get(e['rng'], 'Next'), 15)
                                                                _switch142_index = -1
                                                                if _switch142_index < 0 and strict_equal(_switch142, 0): _switch142_index = 0
                                                                if _switch142_index < 0 and strict_equal(_switch142, 1): _switch142_index = 1
                                                                if _switch142_index < 0 and strict_equal(_switch142, 2): _switch142_index = 2
                                                                if _switch142_index < 0 and strict_equal(_switch142, 3): _switch142_index = 3
                                                                if _switch142_index < 0 and strict_equal(_switch142, 4): _switch142_index = 4
                                                                if _switch142_index < 0 and strict_equal(_switch142, 5): _switch142_index = 5
                                                                if _switch142_index < 0 and strict_equal(_switch142, 6): _switch142_index = 6
                                                                if _switch142_index < 0 and strict_equal(_switch142, 7): _switch142_index = 7
                                                                if _switch142_index < 0 and strict_equal(_switch142, 8): _switch142_index = 8
                                                                if _switch142_index < 0 and strict_equal(_switch142, 9): _switch142_index = 9
                                                                if _switch142_index < 0 and strict_equal(_switch142, 10): _switch142_index = 10
                                                                if _switch142_index < 0 and strict_equal(_switch142, 11): _switch142_index = 11
                                                                if _switch142_index < 0 and strict_equal(_switch142, 12): _switch142_index = 12
                                                                if _switch142_index < 0 and strict_equal(_switch142, 13): _switch142_index = 13
                                                                if _switch142_index < 0 and strict_equal(_switch142, 14): _switch142_index = 14
                                                                if _switch142_index < 0: _switch142_index = -1
                                                                while True:
                                                                    if 0 <= _switch142_index <= 0:
                                                                        put(e['item'], e['c'], get(get(get(e['save'], 'objects'), '_288'), 'name'))
                                                                        put(e['itemQty'], e['c'], 5)
                                                                        break
                                                                    if 0 <= _switch142_index <= 1:
                                                                        put(e['item'], e['c'], get(get(get(e['save'], 'objects'), '_253'), 'name'))
                                                                        put(e['itemQty'], e['c'], 3)
                                                                        break
                                                                    if 0 <= _switch142_index <= 2:
                                                                        if truth(binary('<', call(get(e['rng'], 'NextDouble')), 0.5)):
                                                                            e.set('choices', Array(['_687', '_695']))
                                                                            put(e['item'], e['c'], get(get(get(e['save'], 'objects'), get(e['choices'], call(get(e['rng'], 'Next'), get(e['choices'], 'length')))), 'name'))
                                                                            put(e['basedOnSkill'], e['c'], True)
                                                                        else:
                                                                            put(e['item'], e['c'], get(get(get(e['save'], 'objects'), '_242'), 'name'))
                                                                            put(e['itemQty'], e['c'], 2)
                                                                        break
                                                                    if 0 <= _switch142_index <= 3:
                                                                        put(e['item'], e['c'], get(get(get(e['save'], 'objects'), '_204'), 'name'))
                                                                        put(e['itemQty'], e['c'], 2)
                                                                        break
                                                                    if 0 <= _switch142_index <= 4:
                                                                        put(e['item'], e['c'], get(get(get(e['save'], 'objects'), '_369'), 'name'))
                                                                        put(e['itemQty'], e['c'], 20)
                                                                        break
                                                                    if 0 <= _switch142_index <= 5:
                                                                        put(e['item'], e['c'], get(get(get(e['save'], 'objects'), '_466'), 'name'))
                                                                        put(e['itemQty'], e['c'], 20)
                                                                        break
                                                                    if 0 <= _switch142_index <= 6:
                                                                        put(e['item'], e['c'], get(get(get(e['save'], 'objects'), '_773'), 'name'))
                                                                        put(e['itemQty'], e['c'], 2)
                                                                        break
                                                                    if 0 <= _switch142_index <= 7:
                                                                        put(e['item'], e['c'], get(get(get(e['save'], 'objects'), '_688'), 'name'))
                                                                        put(e['itemQty'], e['c'], 3)
                                                                        break
                                                                    if 0 <= _switch142_index <= 8:
                                                                        put(e['item'], e['c'], get(get(get(e['save'], 'objects'), binary('+', '_', call(get(e['rng'], 'Next'), 628, 634))), 'name'))
                                                                        break
                                                                    if 0 <= _switch142_index <= 9:
                                                                        put(e['item'], e['c'], 'Seasonal Seeds')
                                                                        put(e['itemQty'], e['c'], 20)
                                                                        put(e['noLink'], e['c'], True)
                                                                        break
                                                                    if 0 <= _switch142_index <= 10:
                                                                        if truth(binary('<', call(get(e['rng'], 'NextDouble')), 0.5)):
                                                                            put(e['item'], e['c'], 'Ossified Blade')
                                                                        else:
                                                                            e.set('choices', Array(['_533', '_534']))
                                                                            put(e['item'], e['c'], get(get(get(e['save'], 'objects'), get(e['choices'], call(get(e['rng'], 'Next'), get(e['choices'], 'length')))), 'name'))
                                                                        break
                                                                    if 0 <= _switch142_index <= 11:
                                                                        put(e['item'], e['c'], get(get(get(e['save'], 'objects'), '_621'), 'name'))
                                                                        break
                                                                    if 0 <= _switch142_index <= 12:
                                                                        put(e['item'], e['c'], 'Mystery Box')
                                                                        put(e['itemQty'], e['c'], call(get(e['rng'], 'Next'), 3, 5))
                                                                        break
                                                                    if 0 <= _switch142_index <= 13:
                                                                        put(e['item'], e['c'], get(get(get(e['save'], 'objects'), binary('+', '_SkillBook_', call(get(e['rng'], 'Next'), 5))), 'name'))
                                                                        break
                                                                    if 0 <= _switch142_index <= 14:
                                                                        put(e['item'], e['c'], 'Raccoon Seeds')
                                                                        put(e['itemQty'], e['c'], 8)
                                                                        put(e['noLink'], e['c'], True)
                                                                        break
                                                                    break
                if truth(binary('==', get(e['item'], e['c']), 'None')):
                    _switch143 = call(get(e['rng'], 'Next'), 14)
                    _switch143_index = -1
                    if _switch143_index < 0 and strict_equal(_switch143, 0): _switch143_index = 0
                    if _switch143_index < 0 and strict_equal(_switch143, 1): _switch143_index = 1
                    if _switch143_index < 0 and strict_equal(_switch143, 2): _switch143_index = 2
                    if _switch143_index < 0 and strict_equal(_switch143, 3): _switch143_index = 3
                    if _switch143_index < 0 and strict_equal(_switch143, 4): _switch143_index = 4
                    if _switch143_index < 0 and strict_equal(_switch143, 5): _switch143_index = 5
                    if _switch143_index < 0 and strict_equal(_switch143, 6): _switch143_index = 6
                    if _switch143_index < 0 and strict_equal(_switch143, 7): _switch143_index = 7
                    if _switch143_index < 0 and strict_equal(_switch143, 8): _switch143_index = 8
                    if _switch143_index < 0 and strict_equal(_switch143, 9): _switch143_index = 9
                    if _switch143_index < 0 and strict_equal(_switch143, 10): _switch143_index = 10
                    if _switch143_index < 0 and strict_equal(_switch143, 11): _switch143_index = 11
                    if _switch143_index < 0 and strict_equal(_switch143, 12): _switch143_index = 12
                    if _switch143_index < 0 and strict_equal(_switch143, 13): _switch143_index = 13
                    if _switch143_index < 0: _switch143_index = 14
                    while True:
                        if 0 <= _switch143_index <= 0:
                            put(e['item'], e['c'], get(get(get(e['save'], 'objects'), '_395'), 'name'))
                            put(e['itemQty'], e['c'], 3)
                            break
                        if 0 <= _switch143_index <= 1:
                            put(e['item'], e['c'], get(get(get(e['save'], 'objects'), '_287'), 'name'))
                            put(e['itemQty'], e['c'], 5)
                            break
                        if 0 <= _switch143_index <= 2:
                            put(e['item'], e['c'], 'Seasonal Seeds')
                            put(e['itemQty'], e['c'], 8)
                            put(e['noLink'], e['c'], True)
                            break
                        if 0 <= _switch143_index <= 3:
                            put(e['item'], e['c'], get(get(get(e['save'], 'objects'), binary('+', '_', call(get(e['rng'], 'Next'), 727, 734))), 'name'))
                            break
                        if 0 <= _switch143_index <= 4:
                            e.set('roll', 217)
                            while truth(binary('==', e['roll'], 217)):
                                e.set('roll', call(get(e['rng'], 'Next'), 194, 240))
                            put(e['item'], e['c'], get(get(get(e['save'], 'objects'), binary('+', '_', e['roll'])), 'name'))
                            break
                        if 0 <= _switch143_index <= 5:
                            put(e['item'], e['c'], get(get(get(e['save'], 'objects'), '_709'), 'name'))
                            put(e['itemQty'], e['c'], 10)
                            break
                        if 0 <= _switch143_index <= 6:
                            put(e['item'], e['c'], get(get(get(e['save'], 'objects'), '_369'), 'name'))
                            put(e['itemQty'], e['c'], 10)
                            break
                        if 0 <= _switch143_index <= 7:
                            put(e['item'], e['c'], get(get(get(e['save'], 'objects'), '_466'), 'name'))
                            put(e['itemQty'], e['c'], 10)
                            break
                        if 0 <= _switch143_index <= 8:
                            put(e['item'], e['c'], get(get(get(e['save'], 'objects'), '_688'), 'name'))
                            break
                        if 0 <= _switch143_index <= 9:
                            put(e['item'], e['c'], get(get(get(e['save'], 'objects'), '_689'), 'name'))
                            break
                        if 0 <= _switch143_index <= 10:
                            put(e['item'], e['c'], get(get(get(e['save'], 'objects'), '_770'), 'name'))
                            put(e['itemQty'], e['c'], 10)
                            break
                        if 0 <= _switch143_index <= 11:
                            put(e['item'], e['c'], 'Mixed Flower Seeds')
                            put(e['itemQty'], e['c'], 10)
                            break
                        if 0 <= _switch143_index <= 12:
                            if truth(binary('<', call(get(e['rng'], 'NextDouble')), 0.4)):
                                _switch144 = call(get(e['rng'], 'Next'), 4)
                                _switch144_index = -1
                                if _switch144_index < 0 and strict_equal(_switch144, 0): _switch144_index = 0
                                if _switch144_index < 0 and strict_equal(_switch144, 1): _switch144_index = 1
                                if _switch144_index < 0 and strict_equal(_switch144, 2): _switch144_index = 2
                                if _switch144_index < 0: _switch144_index = 3
                                while True:
                                    if 0 <= _switch144_index <= 0:
                                        put(e['item'], e['c'], get(get(get(e['save'], 'objects'), '_525'), 'name'))
                                        break
                                    if 0 <= _switch144_index <= 1:
                                        put(e['item'], e['c'], get(get(get(e['save'], 'objects'), '_529'), 'name'))
                                        break
                                    if 0 <= _switch144_index <= 2:
                                        put(e['item'], e['c'], get(get(get(e['save'], 'objects'), '_888'), 'name'))
                                        break
                                    if 0 <= _switch144_index <= 3:
                                        put(e['item'], e['c'], get(get(get(e['save'], 'objects'), binary('+', '_', call(get(e['rng'], 'Next'), 531, 533))), 'name'))
                                    break
                            else:
                                put(e['item'], e['c'], 'Mystery Box')
                                put(e['itemQty'], e['c'], 2)
                            break
                        if 0 <= _switch143_index <= 13:
                            put(e['item'], e['c'], get(get(get(e['save'], 'objects'), '_690'), 'name'))
                            break
                        if 0 <= _switch143_index <= 14:
                            put(e['item'], e['c'], get(get(get(e['save'], 'objects'), '_382'), 'name'))
                            break
                        break
                if truth(call(get(e['searchTerm'], 'test'), get(e['item'], e['c']))):
                    if truth(unary('!', call(get(e['searchResults'], 'hasOwnProperty'), get(e['item'], e['c'])))):
                        put(e['searchResults'], get(e['item'], e['c']), Array([Array([]), Array([]), Array([])]))
                    call(get(get(get(e['searchResults'], get(e['item'], e['c'])), e['c']), 'push'), e['numOpened'])
                    update_env(e, 'count', 1, False)
                update_env(e, 'c', 1, False)
            update_env(e, 'numOpened', 1, False)
        call(get(call(get(call(get(e['Object'], 'keys'), e['searchResults']), 'sort')), 'forEach'), Fn(callback_145, e))
        e.set('output', binary('+', e['output'], binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', '<tr><td colspan="', binary('+', e['numColumns'], 1)), '" class="count">Found '), e['count']), ' matching instance(s) of '), get(call(get(e['Object'], 'keys'), e['searchResults']), 'length')), ' matching item(s)</td></tr>\n')))
    else:
        if truth(binary('===', unary('typeof', e['offset']), 'undefined')):
            e.set('offset', binary('*', e['pageSize'], call(get(e['Math'], 'floor'), binary('/', get(get(e['save'], 'mysteryBoxesOpened'), e['whichPlayer']), e['pageSize']))))
        if truth(binary('<', e['offset'], e['pageSize'])):
            call(get(call(e['$'], '#mystery-prev'), 'prop'), 'disabled', True)
        else:
            call(get(call(e['$'], '#mystery-prev'), 'val'), binary('-', e['offset'], e['pageSize']))
            call(get(call(e['$'], '#mystery-prev'), 'prop'), 'disabled', False)
        if truth(binary('<', e['offset'], 100)):
            call(get(call(e['$'], '#mystery-prev-100'), 'prop'), 'disabled', True)
        else:
            call(get(call(e['$'], '#mystery-prev-100'), 'val'), binary('-', e['offset'], 100))
            call(get(call(e['$'], '#mystery-prev-100'), 'prop'), 'disabled', False)
        call(get(call(e['$'], '#mystery-reset'), 'val'), 'reset')
        call(get(call(e['$'], '#mystery-reset'), 'html'), 'Reset Browsing')
        call(get(call(e['$'], '#mystery-next'), 'val'), binary('+', e['offset'], e['pageSize']))
        call(get(call(e['$'], '#mystery-next'), 'prop'), 'disabled', False)
        call(get(call(e['$'], '#mystery-next-100'), 'val'), binary('+', e['offset'], 100))
        call(get(call(e['$'], '#mystery-next-100'), 'prop'), 'disabled', False)
        call(get(call(e['$'], '#mystery-search-text'), 'val'), '')
        call(get(call(e['$'], '#mystery-search-range'), 'val'), 200)
        call(get(call(e['$'], '#mystery-search-all'), 'prop'), 'checked', False)
        e.set('output', binary('+', e['output'], binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', '<table class="output"><thead><tr><th rowspan="2" class="index">Num Open</th>', '<th colspan="2" class="mystery-result">Mystery Box <a href="https://stardewvalleywiki.com/Mystery_Box">'), '<img src="blank.png" class="icon" id="mbox_b"></a></th>'), '<th colspan="2" class="mystery-result">Golden Mystery Box <a href="https://stardewvalleywiki.com/Golden_Mystery_Box">'), '<img src="blank.png" class="icon" id="mbox_g"></a><br/>Without Farming Mastery Perk</th>'), '<th colspan="2" class="mystery-result">Golden Mystery Box <a href="https://stardewvalleywiki.com/Golden_Mystery_Box">'), '<img src="blank.png" class="icon" id="mbox_g"></a><br/>With Farming Mastery Perk</th>')))
        e.set('output', binary('+', e['output'], '</tr>\n<tr>'))
        e.set('c', 0)
        while truth(binary('<', e['c'], e['numColumns'])):
            e.set('output', binary('+', e['output'], '<th class="item">Item</th><th class="qty">Qty</th>'))
            update_env(e, 'c', 1, False)
        e.set('output', binary('+', e['output'], '</tr>\n<tbody>'))
        e.set('g', 1)
        while truth(binary('<=', e['g'], e['pageSize'])):
            e.set('numOpened', binary('+', e['offset'], e['g']))
            e.set('item', Array(['None', 'None', 'None']))
            e.set('itemQty', Array([1, 1, 1]))
            e.set('noLink', Array([False, False, False]))
            e.set('basedOnSkill', Array([False, False, False]))
            e.set('c', 0)
            while truth(binary('<', e['c'], e['numColumns'])):
                e.set('rareMod', (1 if truth(binary('===', e['c'], 0)) else 2))
                e.set('extraBookChance', (0 if truth(get(e['save'], 'gotMysteryBook')) else binary('*', 0.0004, e['numOpened'])))
                if truth(binary('!==', unary('typeof', get(e['save'], 'mp_ids')), 'undefined')):
                    e.set('rng', call(e['CSRandom'], call(e['getRandomSeed'], e['numOpened'], binary('/', get(e['save'], 'gameID'), 2), binary('/', call(e['bigIntToSigned32'], get(get(e['save'], 'mp_ids'), e['whichPlayer'])), 2))))
                else:
                    e.set('rng', call(e['CSRandom'], call(e['getRandomSeed'], e['numOpened'], binary('/', get(e['save'], 'gameID'), 2), 0)))
                    call(get(call(e['$'], '#mystery-note'), 'html'), 'Note: No players found; predictions will not be reliable for game version >= 1.6')
                e.set('prewarm_amount2', call(get(e['rng'], 'Next'), 1, 10))
                e.set('j', 0)
                while truth(binary('<', e['j'], e['prewarm_amount2'])):
                    call(get(e['rng'], 'NextDouble'))
                    update_env(e, 'j', 1, False)
                e.set('prewarm_amount2', call(get(e['rng'], 'Next'), 1, 10))
                e.set('i', 0)
                while truth(binary('<', e['i'], e['prewarm_amount2'])):
                    call(get(e['rng'], 'NextDouble'))
                    update_env(e, 'i', 1, False)
                if truth((_logic147 if truth(_logic147 := binary('>', e['numOpened'], 10)) else binary('>', e['c'], 0))):
                    if truth((binary('<', call(get(e['rng'], 'NextDouble')), 0.005) if truth(_logic148 := binary('==', e['c'], 2)) else _logic148)):
                        put(e['item'], e['c'], 'Golden Animal Cracker')
                    else:
                        if truth((binary('<', call(get(e['rng'], 'NextDouble')), 0.005) if truth(_logic149 := binary('>', e['c'], 0)) else _logic149)):
                            put(e['item'], e['c'], 'Auto-Petter')
                        else:
                            if truth(binary('<', call(get(e['rng'], 'NextDouble')), binary('*', 0.002, e['rareMod']))):
                                put(e['item'], e['c'], get(get(get(e['save'], 'objects'), '_279'), 'name'))
                            else:
                                if truth(binary('<', call(get(e['rng'], 'NextDouble')), binary('*', 0.004, e['rareMod']))):
                                    put(e['item'], e['c'], get(get(get(e['save'], 'objects'), '_74'), 'name'))
                                else:
                                    if truth(binary('<', call(get(e['rng'], 'NextDouble')), binary('*', 0.008, e['rareMod']))):
                                        put(e['item'], e['c'], get(get(get(e['save'], 'objects'), '_166'), 'name'))
                                    else:
                                        if truth(binary('<', call(get(e['rng'], 'NextDouble')), binary('+', binary('*', 0.01, e['rareMod']), e['extraBookChance']))):
                                            if truth(unary('!', get(e['save'], 'gotMysteryBook'))):
                                                put(e['item'], e['c'], get(get(get(e['save'], 'objects'), '_Book_Mystery'), 'name'))
                                            else:
                                                e.set('choices', Array(['_PurpleBook', '_Book_Mystery']))
                                                put(e['item'], e['c'], get(get(get(e['save'], 'objects'), get(e['choices'], call(get(e['rng'], 'Next'), get(e['choices'], 'length')))), 'name'))
                                        else:
                                            if truth(binary('<', call(get(e['rng'], 'NextDouble')), binary('*', 0.01, e['rareMod']))):
                                                e.set('choices', Array(['_797', '_373']))
                                                put(e['item'], e['c'], get(get(get(e['save'], 'objects'), get(e['choices'], call(get(e['rng'], 'Next'), get(e['choices'], 'length')))), 'name'))
                                            else:
                                                if truth(binary('<', call(get(e['rng'], 'NextDouble')), binary('*', 0.01, e['rareMod']))):
                                                    put(e['item'], e['c'], 'Mystery Hat')
                                                else:
                                                    if truth(binary('<', call(get(e['rng'], 'NextDouble')), binary('*', 0.01, e['rareMod']))):
                                                        put(e['item'], e['c'], 'Mystery Shirt')
                                                    else:
                                                        if truth(binary('<', call(get(e['rng'], 'NextDouble')), binary('*', 0.01, e['rareMod']))):
                                                            put(e['item'], e['c'], 'Mystery Wallpaper')
                                                        else:
                                                            if truth((_logic150 if truth(_logic150 := binary('<', call(get(e['rng'], 'NextDouble')), 0.1)) else binary('>', e['c'], 0))):
                                                                _switch151 = call(get(e['rng'], 'Next'), 15)
                                                                _switch151_index = -1
                                                                if _switch151_index < 0 and strict_equal(_switch151, 0): _switch151_index = 0
                                                                if _switch151_index < 0 and strict_equal(_switch151, 1): _switch151_index = 1
                                                                if _switch151_index < 0 and strict_equal(_switch151, 2): _switch151_index = 2
                                                                if _switch151_index < 0 and strict_equal(_switch151, 3): _switch151_index = 3
                                                                if _switch151_index < 0 and strict_equal(_switch151, 4): _switch151_index = 4
                                                                if _switch151_index < 0 and strict_equal(_switch151, 5): _switch151_index = 5
                                                                if _switch151_index < 0 and strict_equal(_switch151, 6): _switch151_index = 6
                                                                if _switch151_index < 0 and strict_equal(_switch151, 7): _switch151_index = 7
                                                                if _switch151_index < 0 and strict_equal(_switch151, 8): _switch151_index = 8
                                                                if _switch151_index < 0 and strict_equal(_switch151, 9): _switch151_index = 9
                                                                if _switch151_index < 0 and strict_equal(_switch151, 10): _switch151_index = 10
                                                                if _switch151_index < 0 and strict_equal(_switch151, 11): _switch151_index = 11
                                                                if _switch151_index < 0 and strict_equal(_switch151, 12): _switch151_index = 12
                                                                if _switch151_index < 0 and strict_equal(_switch151, 13): _switch151_index = 13
                                                                if _switch151_index < 0 and strict_equal(_switch151, 14): _switch151_index = 14
                                                                if _switch151_index < 0: _switch151_index = -1
                                                                while True:
                                                                    if 0 <= _switch151_index <= 0:
                                                                        put(e['item'], e['c'], get(get(get(e['save'], 'objects'), '_288'), 'name'))
                                                                        put(e['itemQty'], e['c'], 5)
                                                                        break
                                                                    if 0 <= _switch151_index <= 1:
                                                                        put(e['item'], e['c'], get(get(get(e['save'], 'objects'), '_253'), 'name'))
                                                                        put(e['itemQty'], e['c'], 3)
                                                                        break
                                                                    if 0 <= _switch151_index <= 2:
                                                                        if truth(binary('<', call(get(e['rng'], 'NextDouble')), 0.5)):
                                                                            e.set('choices', Array(['_687', '_695']))
                                                                            put(e['item'], e['c'], get(get(get(e['save'], 'objects'), get(e['choices'], call(get(e['rng'], 'Next'), get(e['choices'], 'length')))), 'name'))
                                                                            put(e['basedOnSkill'], e['c'], True)
                                                                        else:
                                                                            put(e['item'], e['c'], get(get(get(e['save'], 'objects'), '_242'), 'name'))
                                                                            put(e['itemQty'], e['c'], 2)
                                                                        break
                                                                    if 0 <= _switch151_index <= 3:
                                                                        put(e['item'], e['c'], get(get(get(e['save'], 'objects'), '_204'), 'name'))
                                                                        put(e['itemQty'], e['c'], 2)
                                                                        break
                                                                    if 0 <= _switch151_index <= 4:
                                                                        put(e['item'], e['c'], get(get(get(e['save'], 'objects'), '_369'), 'name'))
                                                                        put(e['itemQty'], e['c'], 20)
                                                                        break
                                                                    if 0 <= _switch151_index <= 5:
                                                                        put(e['item'], e['c'], get(get(get(e['save'], 'objects'), '_466'), 'name'))
                                                                        put(e['itemQty'], e['c'], 20)
                                                                        break
                                                                    if 0 <= _switch151_index <= 6:
                                                                        put(e['item'], e['c'], get(get(get(e['save'], 'objects'), '_773'), 'name'))
                                                                        put(e['itemQty'], e['c'], 2)
                                                                        break
                                                                    if 0 <= _switch151_index <= 7:
                                                                        put(e['item'], e['c'], get(get(get(e['save'], 'objects'), '_688'), 'name'))
                                                                        put(e['itemQty'], e['c'], 3)
                                                                        break
                                                                    if 0 <= _switch151_index <= 8:
                                                                        put(e['item'], e['c'], get(get(get(e['save'], 'objects'), binary('+', '_', call(get(e['rng'], 'Next'), 628, 634))), 'name'))
                                                                        break
                                                                    if 0 <= _switch151_index <= 9:
                                                                        put(e['item'], e['c'], 'Seasonal Seeds')
                                                                        put(e['itemQty'], e['c'], 20)
                                                                        put(e['noLink'], e['c'], True)
                                                                        break
                                                                    if 0 <= _switch151_index <= 10:
                                                                        if truth(binary('<', call(get(e['rng'], 'NextDouble')), 0.5)):
                                                                            put(e['item'], e['c'], 'Ossified Blade')
                                                                        else:
                                                                            e.set('choices', Array(['_533', '_534']))
                                                                            put(e['item'], e['c'], get(get(get(e['save'], 'objects'), get(e['choices'], call(get(e['rng'], 'Next'), get(e['choices'], 'length')))), 'name'))
                                                                        break
                                                                    if 0 <= _switch151_index <= 11:
                                                                        put(e['item'], e['c'], get(get(get(e['save'], 'objects'), '_621'), 'name'))
                                                                        break
                                                                    if 0 <= _switch151_index <= 12:
                                                                        put(e['item'], e['c'], 'Mystery Box')
                                                                        put(e['itemQty'], e['c'], call(get(e['rng'], 'Next'), 3, 5))
                                                                        break
                                                                    if 0 <= _switch151_index <= 13:
                                                                        put(e['item'], e['c'], get(get(get(e['save'], 'objects'), binary('+', '_SkillBook_', call(get(e['rng'], 'Next'), 5))), 'name'))
                                                                        break
                                                                    if 0 <= _switch151_index <= 14:
                                                                        put(e['item'], e['c'], 'Raccoon Seeds')
                                                                        put(e['itemQty'], e['c'], 8)
                                                                        put(e['noLink'], e['c'], True)
                                                                        break
                                                                    break
                if truth(binary('==', get(e['item'], e['c']), 'None')):
                    _switch152 = call(get(e['rng'], 'Next'), 14)
                    _switch152_index = -1
                    if _switch152_index < 0 and strict_equal(_switch152, 0): _switch152_index = 0
                    if _switch152_index < 0 and strict_equal(_switch152, 1): _switch152_index = 1
                    if _switch152_index < 0 and strict_equal(_switch152, 2): _switch152_index = 2
                    if _switch152_index < 0 and strict_equal(_switch152, 3): _switch152_index = 3
                    if _switch152_index < 0 and strict_equal(_switch152, 4): _switch152_index = 4
                    if _switch152_index < 0 and strict_equal(_switch152, 5): _switch152_index = 5
                    if _switch152_index < 0 and strict_equal(_switch152, 6): _switch152_index = 6
                    if _switch152_index < 0 and strict_equal(_switch152, 7): _switch152_index = 7
                    if _switch152_index < 0 and strict_equal(_switch152, 8): _switch152_index = 8
                    if _switch152_index < 0 and strict_equal(_switch152, 9): _switch152_index = 9
                    if _switch152_index < 0 and strict_equal(_switch152, 10): _switch152_index = 10
                    if _switch152_index < 0 and strict_equal(_switch152, 11): _switch152_index = 11
                    if _switch152_index < 0 and strict_equal(_switch152, 12): _switch152_index = 12
                    if _switch152_index < 0 and strict_equal(_switch152, 13): _switch152_index = 13
                    if _switch152_index < 0: _switch152_index = 14
                    while True:
                        if 0 <= _switch152_index <= 0:
                            put(e['item'], e['c'], get(get(get(e['save'], 'objects'), '_395'), 'name'))
                            put(e['itemQty'], e['c'], 3)
                            break
                        if 0 <= _switch152_index <= 1:
                            put(e['item'], e['c'], get(get(get(e['save'], 'objects'), '_287'), 'name'))
                            put(e['itemQty'], e['c'], 5)
                            break
                        if 0 <= _switch152_index <= 2:
                            put(e['item'], e['c'], 'Seasonal Seeds')
                            put(e['itemQty'], e['c'], 8)
                            put(e['noLink'], e['c'], True)
                            break
                        if 0 <= _switch152_index <= 3:
                            put(e['item'], e['c'], get(get(get(e['save'], 'objects'), binary('+', '_', call(get(e['rng'], 'Next'), 727, 734))), 'name'))
                            break
                        if 0 <= _switch152_index <= 4:
                            e.set('roll', 217)
                            while truth(binary('==', e['roll'], 217)):
                                e.set('roll', call(get(e['rng'], 'Next'), 194, 240))
                            put(e['item'], e['c'], get(get(get(e['save'], 'objects'), binary('+', '_', e['roll'])), 'name'))
                            break
                        if 0 <= _switch152_index <= 5:
                            put(e['item'], e['c'], get(get(get(e['save'], 'objects'), '_709'), 'name'))
                            put(e['itemQty'], e['c'], 10)
                            break
                        if 0 <= _switch152_index <= 6:
                            put(e['item'], e['c'], get(get(get(e['save'], 'objects'), '_369'), 'name'))
                            put(e['itemQty'], e['c'], 10)
                            break
                        if 0 <= _switch152_index <= 7:
                            put(e['item'], e['c'], get(get(get(e['save'], 'objects'), '_466'), 'name'))
                            put(e['itemQty'], e['c'], 10)
                            break
                        if 0 <= _switch152_index <= 8:
                            put(e['item'], e['c'], get(get(get(e['save'], 'objects'), '_688'), 'name'))
                            break
                        if 0 <= _switch152_index <= 9:
                            put(e['item'], e['c'], get(get(get(e['save'], 'objects'), '_689'), 'name'))
                            break
                        if 0 <= _switch152_index <= 10:
                            put(e['item'], e['c'], get(get(get(e['save'], 'objects'), '_770'), 'name'))
                            put(e['itemQty'], e['c'], 10)
                            break
                        if 0 <= _switch152_index <= 11:
                            put(e['item'], e['c'], 'Mixed Flower Seeds')
                            put(e['itemQty'], e['c'], 10)
                            break
                        if 0 <= _switch152_index <= 12:
                            if truth(binary('<', call(get(e['rng'], 'NextDouble')), 0.4)):
                                _switch153 = call(get(e['rng'], 'Next'), 4)
                                _switch153_index = -1
                                if _switch153_index < 0 and strict_equal(_switch153, 0): _switch153_index = 0
                                if _switch153_index < 0 and strict_equal(_switch153, 1): _switch153_index = 1
                                if _switch153_index < 0 and strict_equal(_switch153, 2): _switch153_index = 2
                                if _switch153_index < 0: _switch153_index = 3
                                while True:
                                    if 0 <= _switch153_index <= 0:
                                        put(e['item'], e['c'], get(get(get(e['save'], 'objects'), '_525'), 'name'))
                                        break
                                    if 0 <= _switch153_index <= 1:
                                        put(e['item'], e['c'], get(get(get(e['save'], 'objects'), '_529'), 'name'))
                                        break
                                    if 0 <= _switch153_index <= 2:
                                        put(e['item'], e['c'], get(get(get(e['save'], 'objects'), '_888'), 'name'))
                                        break
                                    if 0 <= _switch153_index <= 3:
                                        put(e['item'], e['c'], get(get(get(e['save'], 'objects'), binary('+', '_', call(get(e['rng'], 'Next'), 531, 533))), 'name'))
                                    break
                            else:
                                put(e['item'], e['c'], 'Mystery Box')
                                put(e['itemQty'], e['c'], 2)
                            break
                        if 0 <= _switch152_index <= 13:
                            put(e['item'], e['c'], get(get(get(e['save'], 'objects'), '_690'), 'name'))
                            break
                        if 0 <= _switch152_index <= 14:
                            put(e['item'], e['c'], get(get(get(e['save'], 'objects'), '_382'), 'name'))
                            break
                        break
                update_env(e, 'c', 1, False)
            if truth(binary('===', e['numOpened'], binary('+', get(get(e['save'], 'mysteryBoxesOpened'), e['whichPlayer']), 1))):
                e.set('tclass', 'current')
            else:
                if truth(binary('<=', e['numOpened'], get(get(e['save'], 'mysteryBoxesOpened'), e['whichPlayer']))):
                    e.set('tclass', 'past')
                else:
                    e.set('tclass', 'future')
            e.set('output', binary('+', e['output'], binary('+', binary('+', binary('+', binary('+', '<tr class="', e['tclass']), '"><td>'), call(e['addCommas'], e['numOpened'])), '</td>')))
            e.set('c', 0)
            while truth(binary('<', e['c'], e['numColumns'])):
                e.set('itemIcon', '')
                if truth(get(e['basedOnSkill'], e['c'])):
                    e.set('itemIcon', ' <span data-tooltip="Based on Fishing Skill"><img src="blank.png" class="icon" id="enchant_f" alt="Based on Fishing Skill"></span>')
                e.set('output', binary('+', e['output'], binary('+', binary('+', binary('+', binary('+', binary('+', '<td class="item">', (get(e['item'], e['c']) if truth(get(e['noLink'], e['c'])) else call(e['wikify'], get(e['item'], e['c'])))), e['itemIcon']), '</td><td>'), get(e['itemQty'], e['c'])), '</td>')))
                update_env(e, 'c', 1, False)
            e.set('output', binary('+', e['output'], '</tr>'))
            update_env(e, 'g', 1, False)
    e.set('output', binary('+', e['output'], binary('+', binary('+', binary('+', binary('+', '<tr><td colspan="', binary('+', 1, binary('*', 2, e['numColumns']))), '" class="legend">Note: <img src="blank.png" class="icon" id="enchant_f" alt="Based on Fishing Skill"> denotes items which will only roll if fishing skill is >= 6. If fishing skill is less, this result will instead be '), call(e['wikify'], get(get(get(e['save'], 'objects'), '_242'), 'name'))), ' x2</td></tr>')))
    e.set('output', binary('+', e['output'], '</tbody></table>'))
    return e['output']
    return U


def predictTrains_154(parent, this, args):
    # Upstream predictor: 6933
    e = Env(parent)
    e.declare(['ampm', 'day', 'hour', 'min', 'month', 'monthName', 'output', 'rng', 'tclass', 'thisTrain', 'trainTime', 'week', 'weekDay', 'year'])
    e.local['arguments'] = Array(args)
    e.local['isSearch'] = (args[0] if len(args) > 0 and args[0] is not U else U)
    e.local['offset'] = (args[1] if len(args) > 1 and args[1] is not U else U)
    e.set('output', '')
    if truth((binary('!==', e['offset'], '') if truth(_logic155 := (binary('!==', unary('typeof', e['offset']), 'undefined') if truth(_logic156 := e['isSearch']) else _logic156)) else _logic155)):
        call(get(call(e['$'], '#train-prev'), 'prop'), 'disabled', True)
        call(get(call(e['$'], '#train-next'), 'prop'), 'disabled', True)
        call(get(call(e['$'], '#train-reset'), 'html'), 'Clear Search Results &amp; Reset Browsing')
    else:
        if truth(binary('===', unary('typeof', e['offset']), 'undefined')):
            e.set('offset', binary('*', 28, call(get(e['Math'], 'floor'), binary('/', get(e['save'], 'daysPlayed'), 28))))
        if truth(binary('<', e['offset'], 112)):
            call(get(call(e['$'], '#train-prev-year'), 'prop'), 'disabled', True)
        else:
            call(get(call(e['$'], '#train-prev-year'), 'val'), binary('-', e['offset'], 112))
            call(get(call(e['$'], '#train-prev-year'), 'prop'), 'disabled', False)
        if truth(binary('<', e['offset'], 28)):
            call(get(call(e['$'], '#train-prev-month'), 'prop'), 'disabled', True)
        else:
            call(get(call(e['$'], '#train-prev-month'), 'val'), binary('-', e['offset'], 28))
            call(get(call(e['$'], '#train-prev-month'), 'prop'), 'disabled', False)
        call(get(call(e['$'], '#train-reset'), 'val'), 'reset')
        call(get(call(e['$'], '#train-next-month'), 'val'), binary('+', e['offset'], 28))
        call(get(call(e['$'], '#train-next-year'), 'val'), binary('+', e['offset'], 112))
        e.set('month', call(get(e['Math'], 'floor'), binary('/', e['offset'], 28)))
        e.set('monthName', get(get(e['save'], 'seasonNames'), binary('%', e['month'], 4)))
        e.set('year', binary('+', 1, call(get(e['Math'], 'floor'), binary('/', e['offset'], 112))))
        e.set('output', binary('+', e['output'], binary('+', binary('+', binary('+', binary('+', '<table class="calendar"><thead><tr><th colspan="7">', e['monthName']), ' Year '), e['year']), '</th></tr>\n')))
        e.set('output', binary('+', e['output'], '<tr><th>M</th><th>T</th><th>W</th><th>Th</th><th>F</th><th>Sa</th><th>Su</th></tr></thead>\n<tbody>'))
        e.set('week', 0)
        while truth(binary('<', e['week'], 4)):
            e.set('output', binary('+', e['output'], '<tr>'))
            e.set('weekDay', 1)
            while truth(binary('<', e['weekDay'], 8)):
                e.set('day', binary('+', binary('+', binary('*', 7, e['week']), e['weekDay']), e['offset']))
                if truth(binary('>=', call(e['compareSemVer'], get(e['save'], 'version'), '1.6'), 0)):
                    e.set('rng', call(e['CSRandom'], call(e['getRandomSeed'], binary('+', e['day'], get(e['save'], 'dayAdjust')), binary('/', get(e['save'], 'gameID'), 2))))
                else:
                    e.set('rng', call(e['CSRandom'], binary('+', binary('+', binary('/', get(e['save'], 'gameID'), 2), e['day']), get(e['save'], 'dayAdjust'))))
                if truth(binary('<', e['day'], 31)):
                    e.set('thisTrain', '<span class="none">Railroad<br/>not yet<br/>accessible</span>')
                else:
                    e.set('thisTrain', '<span class="none">&nbsp;<br/>(No train)<br/>&nbsp</span>')
                    if truth(binary('<', call(get(e['rng'], 'NextDouble')), 0.2)):
                        e.set('trainTime', call(get(e['rng'], 'Next'), 900, 1800))
                        e.set('trainTime', binary('-', e['trainTime'], binary('%', e['trainTime'], 10)))
                        e.set('hour', call(get(e['Math'], 'floor'), binary('/', e['trainTime'], 100)))
                        e.set('min', binary('%', e['trainTime'], 100))
                        if truth(binary('<', e['min'], 60)):
                            if truth(binary('>', e['hour'], 12)):
                                e.set('hour', binary('-', e['hour'], 12))
                                e.set('ampm', ' pm')
                            else:
                                if truth(binary('===', e['hour'], 12)):
                                    e.set('ampm', ' pm')
                                else:
                                    e.set('ampm', ' am')
                            if truth(binary('===', e['min'], 0)):
                                e.set('min', '00')
                            e.set('thisTrain', binary('+', binary('+', binary('+', binary('+', '<img src="blank.png" class="event" id="train"><br/>Train at ', e['hour']), ':'), e['min']), e['ampm']))
                if truth(binary('<', e['day'], get(e['save'], 'daysPlayed'))):
                    e.set('tclass', 'past')
                else:
                    if truth(binary('===', e['day'], get(e['save'], 'daysPlayed'))):
                        e.set('tclass', 'current')
                    else:
                        e.set('tclass', 'future')
                e.set('output', binary('+', e['output'], binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', '<td class="', e['tclass']), '"><span class="date"> '), binary('-', e['day'], e['offset'])), '</span><br/>'), '<span class="train cell">'), e['thisTrain']), '</span></td>')))
                update_env(e, 'weekDay', 1, False)
            e.set('output', binary('+', e['output'], '</tr>\n'))
            update_env(e, 'week', 1, False)
        e.set('output', binary('+', e['output'], '</tbody></table>\n'))
    return e['output']
    return U


def callback_170(parent, this, args):
    # Upstream predictor: 7164
    e = Env(parent)
    e.declare([])
    e.local['arguments'] = Array(args)
    e.local['key'] = (args[0] if len(args) > 0 and args[0] is not U else U)
    e.local['index'] = (args[1] if len(args) > 1 and args[1] is not U else U)
    if truth((binary('>', get(get(e['test'], e['key']), 'q'), 0) if truth(_logic171 := binary('>', get(get(e['test'], e['key']), 's'), 0)) else _logic171)):
        call(get(e['console'], 'log'), binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', '** Save id ', e['key']), ' has a giant seasonal on '), get(get(e['test'], e['key']), 's')), ' and a giant qi on '), e['monthName']), ' '), get(get(e['test'], e['key']), 'q')), ', Y'), e['year']))
    return U


def predictNight_157(parent, this, args):
    # Upstream predictor: 7030
    e = Env(parent)
    e.declare(['couldBeWindstorm', 'day', 'extra', 'i', 'month', 'monthName', 'nextRoll', 'output', 'rng', 'tclass', 'test', 'thisEvent', 'week', 'weekDay', 'year'])
    e.local['arguments'] = Array(args)
    e.local['isSearch'] = (args[0] if len(args) > 0 and args[0] is not U else U)
    e.local['offset'] = (args[1] if len(args) > 1 and args[1] is not U else U)
    e.set('output', '')
    if truth((binary('!==', e['offset'], '') if truth(_logic158 := (binary('!==', unary('typeof', e['offset']), 'undefined') if truth(_logic159 := e['isSearch']) else _logic159)) else _logic158)):
        call(get(call(e['$'], '#night-prev'), 'prop'), 'disabled', True)
        call(get(call(e['$'], '#night-next'), 'prop'), 'disabled', True)
        call(get(call(e['$'], '#night-reset'), 'html'), 'Clear Search Results &amp; Reset Browsing')
    else:
        if truth(binary('===', unary('typeof', e['offset']), 'undefined')):
            e.set('offset', binary('*', 28, call(get(e['Math'], 'floor'), binary('/', get(e['save'], 'daysPlayed'), 28))))
        if truth(binary('<', e['offset'], 112)):
            call(get(call(e['$'], '#night-prev-year'), 'prop'), 'disabled', True)
        else:
            call(get(call(e['$'], '#night-prev-year'), 'val'), binary('-', e['offset'], 112))
            call(get(call(e['$'], '#night-prev-year'), 'prop'), 'disabled', False)
        if truth(binary('<', e['offset'], 28)):
            call(get(call(e['$'], '#night-prev-month'), 'prop'), 'disabled', True)
        else:
            call(get(call(e['$'], '#night-prev-month'), 'val'), binary('-', e['offset'], 28))
            call(get(call(e['$'], '#night-prev-month'), 'prop'), 'disabled', False)
        call(get(call(e['$'], '#night-reset'), 'val'), 'reset')
        call(get(call(e['$'], '#night-next-month'), 'val'), binary('+', e['offset'], 28))
        call(get(call(e['$'], '#night-next-year'), 'val'), binary('+', e['offset'], 112))
        e.set('month', call(get(e['Math'], 'floor'), binary('/', e['offset'], 28)))
        e.set('monthName', get(get(e['save'], 'seasonNames'), binary('%', e['month'], 4)))
        e.set('year', binary('+', 1, call(get(e['Math'], 'floor'), binary('/', e['offset'], 112))))
        e.set('output', binary('+', e['output'], binary('+', binary('+', binary('+', binary('+', '<table class="calendar"><thead><tr><th colspan="7">', e['monthName']), ' Year '), e['year']), '</th></tr>\n')))
        e.set('output', binary('+', e['output'], '<tr><th>M</th><th>T</th><th>W</th><th>Th</th><th>F</th><th>Sa</th><th>Su</th></tr></thead>\n<tbody>'))
        e.set('test', Obj({}))
        e.set('week', 0)
        while truth(binary('<', e['week'], 4)):
            e.set('output', binary('+', e['output'], '<tr>'))
            e.set('weekDay', 1)
            while truth(binary('<', e['weekDay'], 8)):
                e.set('day', binary('+', binary('+', binary('*', 7, e['week']), e['weekDay']), e['offset']))
                e.set('couldBeWindstorm', False)
                if truth(binary('===', binary('+', e['day'], get(e['save'], 'dayAdjust')), 30)):
                    e.set('thisEvent', '<img src="blank.png" class="event" id="train"><br/>Earthquake')
                else:
                    if truth(binary('>=', call(e['compareSemVer'], get(e['save'], 'version'), '1.6'), 0)):
                        e.set('rng', call(e['CSRandom'], call(e['getRandomSeed'], binary('+', binary('+', e['day'], 1), get(e['save'], 'dayAdjust')), binary('/', get(e['save'], 'gameID'), 2))))
                        e.set('i', 0)
                        while truth(binary('<', e['i'], 10)):
                            call(get(e['rng'], 'NextDouble'))
                            update_env(e, 'i', 1, False)
                        if truth(get(e['save'], 'greenhouseUnlocked')):
                            e.set('couldBeWindstorm', binary('<', call(get(e['rng'], 'NextDouble')), 0.1))
                        e.set('nextRoll', call(get(e['rng'], 'NextDouble')))
                        if truth(unary('!', get(e['save'], 'greenhouseUnlocked'))):
                            e.set('couldBeWindstorm', binary('<', e['nextRoll'], 0.1))
                        if truth((binary('<', binary('%', e['month'], 4), 3) if truth(_logic160 := binary('<', e['nextRoll'], 0.01)) else _logic160)):
                            e.set('thisEvent', '<img src="blank.png" class="event" id="event_f"><br/>Fairy')
                        else:
                            if truth((binary('>', binary('+', binary('+', e['day'], 1), get(e['save'], 'dayAdjust')), 20) if truth(_logic161 := binary('<', call(get(e['rng'], 'NextDouble')), 0.01)) else _logic161)):
                                e.set('thisEvent', '<img src="blank.png" class="event" id="event_w"><br/>Witch')
                            else:
                                if truth((binary('>', binary('+', binary('+', e['day'], 1), get(e['save'], 'dayAdjust')), 5) if truth(_logic162 := binary('<', call(get(e['rng'], 'NextDouble')), 0.01)) else _logic162)):
                                    e.set('thisEvent', '<img src="blank.png" class="event" id="event_m"><br/>Meteor')
                                else:
                                    if truth(binary('<', call(get(e['rng'], 'NextDouble')), 0.005)):
                                        e.set('thisEvent', '<img src="blank.png" class="event" id="event_o"><br/>Stone Owl')
                                    else:
                                        if truth((binary('>', e['year'], 1) if truth(_logic163 := binary('<', call(get(e['rng'], 'NextDouble')), 0.008)) else _logic163)):
                                            e.set('thisEvent', '<img src="blank.png" class="event" id="event_c"><br/>Strange Capsule')
                                        else:
                                            e.set('thisEvent', '<span class="none">&nbsp;<br/>(No event)<br/>&nbsp</span>')
                    else:
                        e.set('rng', call(e['CSRandom'], binary('+', binary('+', binary('+', binary('/', get(e['save'], 'gameID'), 2), e['day']), 1), get(e['save'], 'dayAdjust'))))
                        if truth((binary('<', call(get(e['rng'], 'NextDouble')), 0.05) if truth(_logic164 := (get(e['save'], 'canHaveChildren') if truth(_logic165 := binary('<', call(e['compareSemVer'], get(e['save'], 'version'), '1.3'), 0)) else _logic165)) else _logic164)):
                            e.set('thisEvent', '<img src="blank.png" class="event" id="event_b"><br/>"Want a Baby?"')
                        else:
                            if truth((binary('<', binary('%', e['month'], 4), 3) if truth(_logic166 := binary('<', call(get(e['rng'], 'NextDouble')), 0.01)) else _logic166)):
                                e.set('thisEvent', '<img src="blank.png" class="event" id="event_f"><br/>Fairy')
                            else:
                                if truth(binary('<', call(get(e['rng'], 'NextDouble')), 0.01)):
                                    e.set('thisEvent', '<img src="blank.png" class="event" id="event_w"><br/>Witch')
                                else:
                                    if truth(binary('<', call(get(e['rng'], 'NextDouble')), 0.01)):
                                        e.set('thisEvent', '<img src="blank.png" class="event" id="event_m"><br/>Meteor')
                                    else:
                                        if truth(binary('<', call(e['compareSemVer'], get(e['save'], 'version'), '1.5'), 0)):
                                            if truth((binary('>', e['year'], 1) if truth(_logic167 := binary('<', call(get(e['rng'], 'NextDouble')), 0.01)) else _logic167)):
                                                e.set('thisEvent', '<img src="blank.png" class="event" id="event_c"><br/>Strange Capsule')
                                            else:
                                                if truth(binary('<', call(get(e['rng'], 'NextDouble')), 0.01)):
                                                    e.set('thisEvent', '<img src="blank.png" class="event" id="event_o"><br/>Stone Owl')
                                                else:
                                                    e.set('thisEvent', '<span class="none">&nbsp;<br/>(No event)<br/>&nbsp</span>')
                                        else:
                                            if truth(binary('<', call(e['compareSemVer'], get(e['save'], 'version'), '1.5.3'), 0)):
                                                if truth((binary('>', e['year'], 1) if truth(_logic168 := binary('<', call(get(e['rng'], 'NextDouble')), 0.008)) else _logic168)):
                                                    e.set('thisEvent', '<img src="blank.png" class="event" id="event_c"><br/>Strange Capsule')
                                                else:
                                                    if truth(binary('<', call(get(e['rng'], 'NextDouble')), 0.008)):
                                                        e.set('thisEvent', '<img src="blank.png" class="event" id="event_o"><br/>Stone Owl')
                                                    else:
                                                        e.set('thisEvent', '<span class="none">&nbsp;<br/>(No event)<br/>&nbsp</span>')
                                            else:
                                                if truth(binary('<', call(get(e['rng'], 'NextDouble')), 0.005)):
                                                    e.set('thisEvent', '<img src="blank.png" class="event" id="event_o"><br/>Stone Owl')
                                                else:
                                                    if truth((binary('>', e['year'], 1) if truth(_logic169 := binary('<', call(get(e['rng'], 'NextDouble')), 0.008)) else _logic169)):
                                                        e.set('thisEvent', '<img src="blank.png" class="event" id="event_c"><br/>Strange Capsule')
                                                    else:
                                                        e.set('thisEvent', '<span class="none">&nbsp;<br/>(No event)<br/>&nbsp</span>')
                if truth(binary('<', e['day'], get(e['save'], 'daysPlayed'))):
                    e.set('tclass', 'past')
                else:
                    if truth(binary('===', e['day'], get(e['save'], 'daysPlayed'))):
                        e.set('tclass', 'current')
                    else:
                        e.set('tclass', 'future')
                e.set('extra', (' <span class="wind"><img alt="Tree Stump" src="blank.png" class="mid" id="stump"></span>' if truth(e['couldBeWindstorm']) else ''))
                e.set('output', binary('+', e['output'], binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', '<td class="', e['tclass']), '"><span class="date"> '), binary('-', e['day'], e['offset'])), '</span>'), e['extra']), '<br/>'), '<span class="night cell">'), e['thisEvent']), '</span></td>')))
                update_env(e, 'weekDay', 1, False)
            e.set('output', binary('+', e['output'], '</tr>\n'))
            update_env(e, 'week', 1, False)
        e.set('output', binary('+', e['output'], '<tr><td colspan="7" class="middle legend"><img src="blank.png" class="mid" alt="Tree Stump" id="stump"> <span>Indicates a day which could be the windstorm that knocks down the big tree in Cindersap Forest (only shows on 1.6 saves)</span></td></tr>'))
        e.set('output', binary('+', e['output'], '</tbody></table>\n'))
        call(get(call(get(e['Object'], 'keys'), e['test']), 'forEach'), Fn(callback_170, e))
    return e['output']
    return U


def predictCrane_172(parent, this, args):
    # Upstream predictor: 7169
    e = Env(parent)
    e.declare(['day', 'month', 'monthName', 'output', 'rng', 'tclass', 'thisEvent', 'week', 'weekDay', 'year'])
    e.local['arguments'] = Array(args)
    e.local['isSearch'] = (args[0] if len(args) > 0 and args[0] is not U else U)
    e.local['offset'] = (args[1] if len(args) > 1 and args[1] is not U else U)
    e.set('output', '')
    if truth((binary('!==', e['offset'], '') if truth(_logic173 := (binary('!==', unary('typeof', e['offset']), 'undefined') if truth(_logic174 := e['isSearch']) else _logic174)) else _logic173)):
        call(get(call(e['$'], '#crane-prev'), 'prop'), 'disabled', True)
        call(get(call(e['$'], '#crane-next'), 'prop'), 'disabled', True)
        call(get(call(e['$'], '#crane-reset'), 'html'), 'Clear Search Results &amp; Reset Browsing')
    else:
        if truth(binary('===', unary('typeof', e['offset']), 'undefined')):
            e.set('offset', binary('*', 28, call(get(e['Math'], 'floor'), binary('/', get(e['save'], 'daysPlayed'), 28))))
        if truth(binary('<', e['offset'], 112)):
            call(get(call(e['$'], '#crane-prev-year'), 'prop'), 'disabled', True)
        else:
            call(get(call(e['$'], '#crane-prev-year'), 'val'), binary('-', e['offset'], 112))
            call(get(call(e['$'], '#crane-prev-year'), 'prop'), 'disabled', False)
        if truth(binary('<', e['offset'], 28)):
            call(get(call(e['$'], '#crane-prev-month'), 'prop'), 'disabled', True)
        else:
            call(get(call(e['$'], '#crane-prev-month'), 'val'), binary('-', e['offset'], 28))
            call(get(call(e['$'], '#crane-prev-month'), 'prop'), 'disabled', False)
        call(get(call(e['$'], '#crane-reset'), 'val'), 'reset')
        call(get(call(e['$'], '#crane-next-month'), 'val'), binary('+', e['offset'], 28))
        call(get(call(e['$'], '#crane-next-year'), 'val'), binary('+', e['offset'], 112))
        e.set('month', call(get(e['Math'], 'floor'), binary('/', e['offset'], 28)))
        e.set('monthName', get(get(e['save'], 'seasonNames'), binary('%', e['month'], 4)))
        e.set('year', binary('+', 1, call(get(e['Math'], 'floor'), binary('/', e['offset'], 112))))
        e.set('output', binary('+', e['output'], binary('+', binary('+', binary('+', binary('+', '<table class="calendar"><thead><tr><th colspan="7">', e['monthName']), ' Year '), e['year']), '</th></tr>\n')))
        e.set('output', binary('+', e['output'], '<tr><th>M</th><th>T</th><th>W</th><th>Th</th><th>F</th><th>Sa</th><th>Su</th></tr></thead>\n<tbody>'))
        e.set('week', 0)
        while truth(binary('<', e['week'], 4)):
            e.set('output', binary('+', e['output'], '<tr>'))
            e.set('weekDay', 1)
            while truth(binary('<', e['weekDay'], 8)):
                e.set('day', binary('+', binary('+', binary('*', 7, e['week']), e['weekDay']), e['offset']))
                if truth(binary('>=', call(e['compareSemVer'], get(e['save'], 'version'), '1.6'), 0)):
                    e.set('rng', call(e['CSRandom'], call(e['getRandomSeed'], get(e['save'], 'gameID'), binary('-', binary('+', e['day'], get(e['save'], 'dayAdjust')), 1))))
                else:
                    e.set('rng', call(e['CSRandom'], binary('-', binary('+', binary('+', get(e['save'], 'gameID'), e['day']), get(e['save'], 'dayAdjust')), 1)))
                if truth((binary('<', call(get(e['rng'], 'NextDouble')), 0.25) if truth(_logic175 := binary('>=', call(e['compareSemVer'], get(e['save'], 'version'), '1.4'), 0)) else _logic175)):
                    e.set('thisEvent', '<span class="none"><img src="blank.png" class="tall" id="movie_gs"><br/>(Game In Use)</span>')
                else:
                    e.set('thisEvent', 'Game Can<br/>Be Played<br>&nbsp;')
                if truth(binary('<', e['day'], get(e['save'], 'daysPlayed'))):
                    e.set('tclass', 'past')
                else:
                    if truth(binary('===', e['day'], get(e['save'], 'daysPlayed'))):
                        e.set('tclass', 'current')
                    else:
                        e.set('tclass', 'future')
                e.set('output', binary('+', e['output'], binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', '<td class="', e['tclass']), '"><span class="date"> '), binary('-', e['day'], e['offset'])), '</span><br/>'), '<span class="crane cell">'), e['thisEvent']), '</span></td>')))
                update_env(e, 'weekDay', 1, False)
            e.set('output', binary('+', e['output'], '</tr>\n'))
            update_env(e, 'week', 1, False)
        e.set('output', binary('+', e['output'], '</tbody></table>\n'))
    return e['output']
    return U


def predictResortVisitors_176(parent, this, args):
    # Upstream predictor: 7243
    e = Env(parent)
    e.declare(['children', 'day', 'dayOfYear', 'failed', 'festival', 'group', 'groups', 'i', 'keys', 'month', 'monthName', 'output', 'rng', 'tclass', 'thisEvent', 'valid', 'validVisitors', 'visitors', 'week', 'weekDay', 'who', 'year'])
    e.local['arguments'] = Array(args)
    e.local['isSearch'] = (args[0] if len(args) > 0 and args[0] is not U else U)
    e.local['offset'] = (args[1] if len(args) > 1 and args[1] is not U else U)
    e.set('output', '')
    e.set('children', Obj({'Jas': 1, 'Vincent': 1, 'Leo': 1}))
    e.set('groups', table(13))
    if truth(binary('===', unary('typeof', e['offset']), 'undefined')):
        e.set('offset', binary('*', 28, call(get(e['Math'], 'floor'), binary('/', get(e['save'], 'daysPlayed'), 28))))
    if truth(binary('<', e['offset'], 112)):
        call(get(call(e['$'], '#resort-prev-year'), 'prop'), 'disabled', True)
    else:
        call(get(call(e['$'], '#resort-prev-year'), 'val'), binary('-', e['offset'], 112))
        call(get(call(e['$'], '#resort-prev-year'), 'prop'), 'disabled', False)
    if truth(binary('<', e['offset'], 28)):
        call(get(call(e['$'], '#resort-prev-month'), 'prop'), 'disabled', True)
    else:
        call(get(call(e['$'], '#resort-prev-month'), 'val'), binary('-', e['offset'], 28))
        call(get(call(e['$'], '#resort-prev-month'), 'prop'), 'disabled', False)
    call(get(call(e['$'], '#resort-reset'), 'val'), 'reset')
    call(get(call(e['$'], '#resort-next-month'), 'val'), binary('+', e['offset'], 28))
    call(get(call(e['$'], '#resort-next-year'), 'val'), binary('+', e['offset'], 112))
    e.set('month', call(get(e['Math'], 'floor'), binary('/', e['offset'], 28)))
    e.set('monthName', get(get(e['save'], 'seasonNames'), binary('%', e['month'], 4)))
    e.set('year', binary('+', 1, call(get(e['Math'], 'floor'), binary('/', e['offset'], 112))))
    e.set('output', binary('+', e['output'], binary('+', binary('+', binary('+', binary('+', '<table class="calendar"><thead><tr><th colspan="7">', e['monthName']), ' Year '), e['year']), '</th></tr>\n')))
    e.set('output', binary('+', e['output'], '<tr><th>M</th><th>T</th><th>W</th><th>Th</th><th>F</th><th>Sa</th><th>Su</th></tr></thead>\n<tbody>'))
    e.set('week', 0)
    while truth(binary('<', e['week'], 4)):
        e.set('output', binary('+', e['output'], '<tr>'))
        e.set('weekDay', 1)
        while truth(binary('<', e['weekDay'], 8)):
            e.set('visitors', Array([]))
            e.set('day', binary('+', binary('+', binary('*', 7, e['week']), e['weekDay']), e['offset']))
            e.set('festival', '')
            _switch177 = binary('%', e['day'], 112)
            _switch177_index = -1
            if _switch177_index < 0 and strict_equal(_switch177, 13): _switch177_index = 0
            if _switch177_index < 0 and strict_equal(_switch177, 24): _switch177_index = 1
            if _switch177_index < 0 and strict_equal(_switch177, 39): _switch177_index = 2
            if _switch177_index < 0 and strict_equal(_switch177, 56): _switch177_index = 3
            if _switch177_index < 0 and strict_equal(_switch177, 72): _switch177_index = 4
            if _switch177_index < 0 and strict_equal(_switch177, 83): _switch177_index = 5
            if _switch177_index < 0 and strict_equal(_switch177, 92): _switch177_index = 6
            if _switch177_index < 0 and strict_equal(_switch177, 109): _switch177_index = 7
            if _switch177_index < 0: _switch177_index = -1
            while True:
                if 0 <= _switch177_index <= 0:
                    e.set('festival', 'Egg Festival')
                    break
                if 0 <= _switch177_index <= 1:
                    e.set('festival', 'Flower Dance')
                    break
                if 0 <= _switch177_index <= 2:
                    e.set('festival', 'Luau')
                    break
                if 0 <= _switch177_index <= 3:
                    e.set('festival', 'Moonlight Jellies')
                    break
                if 0 <= _switch177_index <= 4:
                    e.set('festival', 'Valley Fair')
                    break
                if 0 <= _switch177_index <= 5:
                    e.set('festival', "Spirit's Eve")
                    break
                if 0 <= _switch177_index <= 6:
                    e.set('festival', 'Ice Festival')
                    break
                if 0 <= _switch177_index <= 7:
                    e.set('festival', 'Winter Star')
                    break
                break
            if truth(binary('!==', e['festival'], '')):
                e.set('thisEvent', binary('+', binary('+', '<span class="none">Closed for<br/>', e['festival']), '</span>'))
            else:
                e.set('rng', call(e['CSRandom'], binary('+', binary('*', 1.21, get(e['save'], 'gameID')), binary('*', 2.5, binary('+', e['day'], get(e['save'], 'dayAdjust'))))))
                e.set('validVisitors', Obj({}))
                e.set('visitors', Array([]))
                e.set('i', 0)
                while truth(binary('<', e['i'], get(get(e['save'], 'characters'), 'length'))):
                    e.set('who', get(get(e['save'], 'characters'), e['i']))
                    e.set('valid', True)
                    if truth(((_logic179 if truth(_logic179 := (_logic180 if truth(_logic180 := binary('===', e['weekDay'], 2)) else binary('===', e['weekDay'], 3))) else binary('===', e['weekDay'], 5)) if truth(_logic178 := (_logic181 if truth(_logic181 := (_logic182 if truth(_logic182 := binary('===', e['who'], 'Penny')) else binary('===', e['who'], 'Jas'))) else binary('===', e['who'], 'Vincent'))) else _logic178)):
                        e.set('valid', False)
                    else:
                        if truth(((_logic184 if truth(_logic184 := binary('===', e['weekDay'], 2)) else binary('===', e['weekDay'], 4)) if truth(_logic183 := (_logic185 if truth(_logic185 := binary('===', e['who'], 'Harvey')) else binary('===', e['who'], 'Maru'))) else _logic183)):
                            e.set('valid', False)
                        else:
                            if truth((binary('!==', e['weekDay'], 5) if truth(_logic186 := binary('===', e['who'], 'Clint')) else _logic186)):
                                e.set('valid', False)
                            else:
                                if truth((binary('!==', e['weekDay'], 2) if truth(_logic187 := binary('===', e['who'], 'Robin')) else _logic187)):
                                    e.set('valid', False)
                                else:
                                    if truth(((_logic189 if truth(_logic189 := binary('!==', e['weekDay'], 1)) else binary('!==', e['weekDay'], 2)) if truth(_logic188 := binary('===', e['who'], 'Marnie')) else _logic188)):
                                        e.set('valid', False)
                                    else:
                                        if truth((_logic190 if truth(_logic190 := (_logic191 if truth(_logic191 := (_logic192 if truth(_logic192 := (_logic193 if truth(_logic193 := (_logic194 if truth(_logic194 := (_logic195 if truth(_logic195 := (_logic196 if truth(_logic196 := binary('===', e['who'], 'Sandy')) else binary('===', e['who'], 'Dwarf'))) else binary('===', e['who'], 'Krobus'))) else binary('===', e['who'], 'Wizard'))) else binary('===', e['who'], 'Linus'))) else binary('===', e['who'], 'Willy'))) else binary('===', e['who'], 'Evelyn'))) else binary('===', e['who'], 'George'))):
                                            e.set('valid', False)
                                        else:
                                            e.set('dayOfYear', binary('%', e['day'], 112))
                                            if truth((binary('===', e['dayOfYear'], 4) if truth(_logic197 := binary('===', e['who'], 'Abigail')) else _logic197)):
                                                e.set('valid', False)
                                            else:
                                                if truth((binary('===', e['dayOfYear'], 44) if truth(_logic198 := binary('===', e['who'], 'Alex')) else _logic198)):
                                                    e.set('valid', False)
                                                else:
                                                    if truth((binary('===', e['dayOfYear'], 81) if truth(_logic199 := binary('===', e['who'], 'Caroline')) else _logic199)):
                                                        e.set('valid', False)
                                                    else:
                                                        if truth((binary('===', e['dayOfYear'], 100) if truth(_logic200 := binary('===', e['who'], 'Clint')) else _logic200)):
                                                            e.set('valid', False)
                                                        else:
                                                            if truth((binary('===', e['dayOfYear'], 53) if truth(_logic201 := binary('===', e['who'], 'Demetrius')) else _logic201)):
                                                                e.set('valid', False)
                                                            else:
                                                                if truth((binary('===', e['dayOfYear'], 37) if truth(_logic202 := binary('===', e['who'], 'Elliott')) else _logic202)):
                                                                    e.set('valid', False)
                                                                else:
                                                                    if truth((binary('===', e['dayOfYear'], 95) if truth(_logic203 := binary('===', e['who'], 'Emily')) else _logic203)):
                                                                        e.set('valid', False)
                                                                    else:
                                                                        if truth((binary('===', e['dayOfYear'], 60) if truth(_logic204 := binary('===', e['who'], 'Gus')) else _logic204)):
                                                                            e.set('valid', False)
                                                                        else:
                                                                            if truth((binary('===', e['dayOfYear'], 93) if truth(_logic205 := binary('===', e['who'], 'Haley')) else _logic205)):
                                                                                e.set('valid', False)
                                                                            else:
                                                                                if truth((binary('===', e['dayOfYear'], 99) if truth(_logic206 := binary('===', e['who'], 'Harvey')) else _logic206)):
                                                                                    e.set('valid', False)
                                                                                else:
                                                                                    if truth((binary('===', e['dayOfYear'], 102) if truth(_logic207 := binary('===', e['who'], 'Jas')) else _logic207)):
                                                                                        e.set('valid', False)
                                                                                    else:
                                                                                        if truth(((_logic209 if truth(_logic209 := binary('===', e['dayOfYear'], 11)) else binary('===', e['dayOfYear'], 18)) if truth(_logic208 := binary('===', e['who'], 'Jodi')) else _logic208)):
                                                                                            e.set('valid', False)
                                                                                        else:
                                                                                            if truth((binary('===', e['dayOfYear'], 16) if truth(_logic210 := binary('===', e['who'], 'Leah')) else _logic210)):
                                                                                                e.set('valid', False)
                                                                                            else:
                                                                                                if truth((binary('===', e['dayOfYear'], 65) if truth(_logic211 := binary('===', e['who'], 'Lewis')) else _logic211)):
                                                                                                    e.set('valid', False)
                                                                                                else:
                                                                                                    if truth(((_logic213 if truth(_logic213 := binary('===', e['dayOfYear'], 102)) else binary('===', e['dayOfYear'], 74)) if truth(_logic212 := binary('===', e['who'], 'Marnie')) else _logic212)):
                                                                                                        e.set('valid', False)
                                                                                                    else:
                                                                                                        if truth((binary('===', e['dayOfYear'], 25) if truth(_logic214 := binary('===', e['who'], 'Pam')) else _logic214)):
                                                                                                            e.set('valid', False)
                                                                                                        else:
                                                                                                            if truth((binary('===', e['dayOfYear'], 88) if truth(_logic215 := binary('===', e['who'], 'Penny')) else _logic215)):
                                                                                                                e.set('valid', False)
                                                                                                            else:
                                                                                                                if truth((binary('===', e['dayOfYear'], 44) if truth(_logic216 := binary('===', e['who'], 'Robin')) else _logic216)):
                                                                                                                    e.set('valid', False)
                                                                                                                else:
                                                                                                                    if truth((binary('===', e['dayOfYear'], 67) if truth(_logic217 := binary('===', e['who'], 'Sam')) else _logic217)):
                                                                                                                        e.set('valid', False)
                                                                                                                    else:
                                                                                                                        if truth((binary('===', e['dayOfYear'], 32) if truth(_logic218 := binary('===', e['who'], 'Sebastian')) else _logic218)):
                                                                                                                            e.set('valid', False)
                                                                                                                        else:
                                                                                                                            if truth((binary('===', e['dayOfYear'], 11) if truth(_logic219 := binary('===', e['who'], 'Vincent')) else _logic219)):
                                                                                                                                e.set('valid', False)
                    if truth(e['valid']):
                        put(e['validVisitors'], e['who'], 1)
                    update_env(e, 'i', 1, False)
                if truth(binary('<', call(get(e['rng'], 'NextDouble')), 0.4)):
                    e.set('i', 0)
                    while truth(binary('<', e['i'], binary('-', 5, get(e['visitors'], 'length')))):
                        e.set('keys', call(get(e['Object'], 'keys'), e['validVisitors']))
                        e.set('who', get(e['keys'], call(get(e['rng'], 'Next'), get(e['keys'], 'length'))))
                        if truth(unary('!', call(get(e['children'], 'hasOwnProperty'), e['who']))):
                            delete(e['validVisitors'], e['who'])
                            call(get(e['visitors'], 'push'), e['who'])
                        update_env(e, 'i', 1, False)
                else:
                    e.set('group', get(e['groups'], call(get(e['rng'], 'Next'), get(e['groups'], 'length'))))
                    e.set('failed', False)
                    e.set('i', 0)
                    while truth(binary('<', e['i'], get(e['group'], 'length'))):
                        if truth(unary('!', call(get(e['validVisitors'], 'hasOwnProperty'), get(e['group'], e['i'])))):
                            e.set('failed', True)
                            break
                        update_env(e, 'i', 1, False)
                    if truth(unary('!', e['failed'])):
                        e.set('i', 0)
                        while truth(binary('<', e['i'], get(e['group'], 'length'))):
                            delete(e['validVisitors'], get(e['group'], e['i']))
                            call(get(e['visitors'], 'push'), get(e['group'], e['i']))
                            update_env(e, 'i', 1, False)
                    e.set('i', 0)
                    while truth(binary('<', e['i'], binary('-', 5, get(e['visitors'], 'length')))):
                        e.set('keys', call(get(e['Object'], 'keys'), e['validVisitors']))
                        e.set('who', get(e['keys'], call(get(e['rng'], 'Next'), get(e['keys'], 'length'))))
                        if truth(unary('!', call(get(e['children'], 'hasOwnProperty'), e['who']))):
                            delete(e['validVisitors'], e['who'])
                            call(get(e['visitors'], 'push'), e['who'])
                        update_env(e, 'i', 1, False)
                e.set('thisEvent', call(get(e['visitors'], 'join'), ',<br/>'))
            if truth(binary('<', e['day'], get(e['save'], 'daysPlayed'))):
                e.set('tclass', 'past')
            else:
                if truth(binary('===', e['day'], get(e['save'], 'daysPlayed'))):
                    e.set('tclass', 'current')
                else:
                    e.set('tclass', 'future')
            e.set('output', binary('+', e['output'], binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', '<td class="', e['tclass']), '"><span class="date"> '), binary('-', e['day'], e['offset'])), '</span><br/>'), '<span class="resort cell">'), e['thisEvent']), '</span></td>')))
            update_env(e, 'weekDay', 1, False)
        e.set('output', binary('+', e['output'], '</tr>\n'))
        update_env(e, 'week', 1, False)
    e.set('output', binary('+', e['output'], '</tbody></table>\n'))
    return e['output']
    return U


def predictEnchantments_220(parent, this, args):
    # Upstream predictor: 7436
    e = Env(parent)
    e.declare(['bigPageSize', 'c', 'count', 'e', 'g', 'i', 'item', 'j', 'labels', 'next', 'numColumns', 'o', 'output', 'pageSize', 'player', 'prefix', 'randRoll', 'result', 'result2', 'result3', 'rng', 'roll', 'roll2', 'roll3', 'searchEnd', 'searchResults', 'searchStart', 'searchTerm', 'tclass', 'timesEnchanted', 'tooltip', 'validEnchants', 'whichPlayer'])
    e.local['arguments'] = Array(args)
    e.local['isSearch'] = (args[0] if len(args) > 0 and args[0] is not U else U)
    e.local['offset'] = (args[1] if len(args) > 1 and args[1] is not U else U)
    e.set('output', '')
    e.set('pageSize', 20)
    e.set('bigPageSize', 100)
    e.set('labels', Array(['Weapon', 'Pickaxe', 'Axe', 'Hoe', 'Watering Can', 'Fishing Rod', 'Pan']))
    e.set('numColumns', get(e['labels'], 'length'))
    e.set('validEnchants', table(14))
    if truth((binary('!==', e['offset'], '') if truth(_logic221 := (binary('!==', unary('typeof', e['offset']), 'undefined') if truth(_logic222 := e['isSearch']) else _logic222)) else _logic221)):
        pass
    else:
        e.set('whichPlayer', 0)
        if truth((binary('>', get(get(e['save'], 'mp_ids'), 'length'), 1) if truth(_logic223 := binary('!==', unary('typeof', get(e['save'], 'mp_ids')), 'undefined')) else _logic223)):
            call(get(call(e['$'], '#enchant-player'), 'show'))
            if truth(binary('==', get(call(e['$'], '#enchant-player-select option'), 'length'), 0)):
                e.set('player', 0)
                while truth(binary('<', e['player'], get(get(e['save'], 'mp_ids'), 'length'))):
                    e.set('prefix', ('Main Farmer ' if truth(binary('==', e['player'], 0)) else 'Farmhand '))
                    e.set('o', call(e['Option'], binary('+', e['prefix'], get(get(e['save'], 'names'), e['player'])), e['player']))
                    if truth(binary('==', e['player'], 0)):
                        put(e['o'], 'selected', True)
                    call(get(call(e['$'], '#enchant-player-select'), 'append'), e['o'])
                    update_env(e, 'player', 1, False)
            else:
                e.set('whichPlayer', call(get(call(e['$'], '#enchant-player-select'), 'val')))
        else:
            call(get(call(e['$'], '#enchant-player'), 'hide'))
        if truth(binary('===', unary('typeof', e['offset']), 'undefined')):
            e.set('offset', binary('*', e['pageSize'], call(get(e['Math'], 'floor'), binary('/', get(get(e['save'], 'timesEnchanted'), e['whichPlayer']), e['pageSize']))))
        if truth(binary('<', e['offset'], e['pageSize'])):
            call(get(call(e['$'], '#enchant-prev'), 'prop'), 'disabled', True)
        else:
            call(get(call(e['$'], '#enchant-prev'), 'val'), binary('-', e['offset'], e['pageSize']))
            call(get(call(e['$'], '#enchant-prev'), 'prop'), 'disabled', False)
        if truth(binary('<', e['offset'], e['bigPageSize'])):
            call(get(call(e['$'], '#enchant-prev-big'), 'prop'), 'disabled', True)
        else:
            call(get(call(e['$'], '#enchant-prev-big'), 'val'), binary('-', e['offset'], e['bigPageSize']))
            call(get(call(e['$'], '#enchant-prev-big'), 'prop'), 'disabled', False)
        call(get(call(e['$'], '#enchant-reset'), 'val'), 'reset')
        call(get(call(e['$'], '#enchant-reset'), 'html'), 'Reset Browsing')
        call(get(call(e['$'], '#enchant-next'), 'val'), binary('+', e['offset'], e['pageSize']))
        call(get(call(e['$'], '#enchant-next'), 'prop'), 'disabled', False)
        call(get(call(e['$'], '#enchant-next-big'), 'val'), binary('+', e['offset'], e['bigPageSize']))
        call(get(call(e['$'], '#enchant-next-big'), 'prop'), 'disabled', False)
        e.set('output', binary('+', e['output'], binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', '<table class="output"><thead><tr><th class="index">Num Ench.</th>', '<th class="enchant-result item">Weapon <a href="https://stardewvalleywiki.com/Weapons">'), '<img src="blank.png" class="dark icon" id="enchant_w"></a></th>'), '<th class="enchant-result item">Pickaxe <a href="https://stardewvalleywiki.com/Pickaxes">'), '<img src="blank.png" class="dark icon" id="enchant_p"></a></th>'), '<th class="enchant-result item">Axe <a href="https://stardewvalleywiki.com/Axes">'), '<img src="blank.png" class="dark icon" id="enchant_a"></a></th>'), '<th class="enchant-result item">Hoe <a href="https://stardewvalleywiki.com/Hoes">'), '<img src="blank.png" class="dark icon" id="enchant_h"></a></th>'), '<th class="enchant-result item">Watering Can <a href="https://stardewvalleywiki.com/Watering_Cans">'), '<img src="blank.png" class="dark icon" id="enchant_c"></a></th>'), '<th class="enchant-result">Fishing Rod <a href="https://stardewvalleywiki.com/Fishing_Rods">'), '<img src="blank.png" class="dark icon" id="enchant_f"></a></th>'), '<th class="enchant-result">Pan <a href="https://stardewvalleywiki.com/Pans">'), '<img src="blank.png" class="dark icon" id="enchant_n"></a></th>')))
        e.set('output', binary('+', e['output'], '</tr>\n<tbody>'))
        e.set('g', 1)
        while truth(binary('<=', e['g'], e['pageSize'])):
            e.set('timesEnchanted', binary('+', e['offset'], e['g']))
            e.set('item', Array([]))
            e.set('tooltip', Array([]))
            if truth(binary('>=', call(e['compareSemVer'], get(e['save'], 'version'), '1.6'), 0)):
                if truth(binary('!==', unary('typeof', get(e['save'], 'mp_ids')), 'undefined')):
                    e.set('rng', call(e['CSRandom'], call(e['getRandomSeedFromBigInts'], call(e['bigInt'], binary('-', e['timesEnchanted'], 1)), call(e['bigInt'], get(e['save'], 'gameID')), get(get(e['save'], 'mp_ids'), e['whichPlayer']))))
                else:
                    e.set('rng', call(e['CSRandom'], call(e['getRandomSeed'], binary('-', e['timesEnchanted'], 1), get(e['save'], 'gameID'), 0)))
                    call(get(call(e['$'], '#enchant-note'), 'html'), 'Note: No players found; predictions will not be reliable for game version >= 1.6')
            else:
                e.set('rng', call(e['CSRandom'], binary('-', binary('+', e['timesEnchanted'], get(e['save'], 'gameID')), 1)))
            e.set('randRoll', call(get(e['rng'], 'NextDouble')))
            e.set('c', 0)
            while truth(binary('<', e['c'], e['numColumns'])):
                e.set('roll', call(get(e['Math'], 'floor'), binary('*', e['randRoll'], get(get(e['validEnchants'], e['c']), 'length'))))
                e.set('result', get(get(e['validEnchants'], e['c']), e['roll']))
                put(e['item'], e['c'], Array([call(e['wikify'], e['result'])]))
                put(e['tooltip'], e['c'], binary('+', binary('+', binary('+', binary('+', binary('+', get(e['labels'], e['c']), ' enchant ('), e['g']), ')\n\nNone &#x2192; '), e['result']), '\n\n'))
                e.set('roll2', call(get(e['Math'], 'floor'), binary('*', e['randRoll'], binary('-', get(get(e['validEnchants'], e['c']), 'length'), 1))))
                if truth(binary('<', e['roll2'], e['roll'])):
                    call(get(get(e['item'], e['c']), 'push'), call(e['wikify'], get(get(e['validEnchants'], e['c']), e['roll2'])))
                else:
                    call(get(get(e['item'], e['c']), 'push'), call(e['wikify'], get(get(e['validEnchants'], e['c']), binary('+', e['roll2'], 1))))
                e.set('roll3', call(get(e['Math'], 'floor'), binary('*', e['randRoll'], binary('-', get(get(e['validEnchants'], e['c']), 'length'), 2))))
                if truth(binary('<', e['roll3'], e['roll2'])):
                    call(get(get(e['item'], e['c']), 'push'), call(e['wikify'], get(get(e['validEnchants'], e['c']), e['roll3'])))
                else:
                    call(get(get(e['item'], e['c']), 'push'), call(e['wikify'], get(get(e['validEnchants'], e['c']), binary('+', e['roll3'], 2))))
                e.set('e', 0)
                while truth(binary('<', e['e'], get(get(e['validEnchants'], e['c']), 'length'))):
                    e.set('i', binary('+', e['roll2'], (1 if truth(binary('<=', e['e'], e['roll2'])) else 0)))
                    e.set('result2', get(get(e['validEnchants'], e['c']), e['i']))
                    e.set('j', binary('+', e['roll3'], (1 if truth(binary('<=', e['e'], e['roll3'])) else 0)))
                    if truth(binary('===', e['i'], e['j'])):
                        update_env(e, 'j', 1, False)
                        if truth(binary('===', e['e'], e['j'])):
                            update_env(e, 'j', 1, False)
                    e.set('result3', get(get(e['validEnchants'], e['c']), e['j']))
                    put(e['tooltip'], e['c'], binary('+', get(e['tooltip'], e['c']), binary('+', binary('+', binary('+', binary('+', binary('+', get(get(e['validEnchants'], e['c']), e['e']), ' &#x2192; '), e['result2']), ' or '), e['result3']), '\n')))
                    update_env(e, 'e', 1, False)
                update_env(e, 'c', 1, False)
            if truth(binary('===', e['timesEnchanted'], binary('+', get(get(e['save'], 'timesEnchanted'), e['whichPlayer']), 1))):
                e.set('tclass', 'current')
            else:
                if truth(binary('<=', e['timesEnchanted'], get(get(e['save'], 'timesEnchanted'), e['whichPlayer']))):
                    e.set('tclass', 'past')
                else:
                    e.set('tclass', 'future')
            e.set('output', binary('+', e['output'], binary('+', binary('+', binary('+', binary('+', '<tr class="', e['tclass']), '"><td>'), call(e['addCommas'], e['timesEnchanted'])), '</td>')))
            e.set('c', 0)
            while truth(binary('<', e['c'], e['numColumns'])):
                e.set('output', binary('+', e['output'], binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', '<td class="item">', get(get(e['item'], e['c']), 0)), ', '), get(get(e['item'], e['c']), 1)), '<br/>or '), get(get(e['item'], e['c']), 2)), '<br/><span class="note" data-tooltip="'), get(e['tooltip'], e['c'])), '">(...)</span></td>')))
                update_env(e, 'c', 1, False)
            e.set('output', binary('+', e['output'], '</tr>'))
            update_env(e, 'g', 1, False)
    e.set('output', binary('+', e['output'], '</tbody></table>'))
    return e['output']
    return U


def predictMineChests_224(parent, this, args):
    # Upstream predictor: 7601
    e = Env(parent)
    e.declare(['choices', 'floor', 'item', 'output', 'rng'])
    e.local['arguments'] = Array(args)
    e.local['isSearch'] = (args[0] if len(args) > 0 and args[0] is not U else U)
    e.local['offset'] = (args[1] if len(args) > 1 and args[1] is not U else U)
    e.set('output', '')
    e.set('choices', Obj({'10': Array([get(get(e['save'], 'boots'), 506), get(get(e['save'], 'boots'), 507), get(get(e['save'], 'weapons'), 12), get(get(e['save'], 'weapons'), 17), get(get(e['save'], 'weapons'), 22), get(get(e['save'], 'weapons'), 31)]), '20': Array([get(get(e['save'], 'weapons'), 11), get(get(e['save'], 'weapons'), 24), get(get(e['save'], 'weapons'), 20), get(get(get(e['save'], 'objects'), '_517'), 'name'), get(get(get(e['save'], 'objects'), '_519'), 'name')]), '30': Array(['(No chest)']), '40': Array([get(get(e['save'], 'weapons'), 32)]), '50': Array([get(get(e['save'], 'boots'), 509), get(get(e['save'], 'boots'), 510), get(get(e['save'], 'boots'), 508), get(get(e['save'], 'weapons'), 1), get(get(e['save'], 'weapons'), 43)]), '60': Array([get(get(e['save'], 'weapons'), 21), get(get(e['save'], 'weapons'), 44), get(get(e['save'], 'weapons'), 6), get(get(e['save'], 'weapons'), 18), get(get(e['save'], 'weapons'), 27)]), '70': Array([get(get(e['save'], 'weapons'), 33)]), '80': Array([get(get(e['save'], 'boots'), 512), get(get(e['save'], 'boots'), 511), get(get(e['save'], 'weapons'), 10), get(get(e['save'], 'weapons'), 7), get(get(e['save'], 'weapons'), 46), get(get(e['save'], 'weapons'), 19)]), '90': Array([get(get(e['save'], 'weapons'), 8), get(get(e['save'], 'weapons'), 52), get(get(e['save'], 'weapons'), 45), get(get(e['save'], 'weapons'), 5), get(get(e['save'], 'weapons'), 60)]), '100': Array(['Stardrop']), '110': Array([get(get(e['save'], 'boots'), 514), get(get(e['save'], 'boots'), 878), get(get(e['save'], 'weapons'), 50), get(get(e['save'], 'weapons'), 28)]), '120': Array(['Skull Key'])}))
    e.set('output', binary('+', e['output'], '<table class="output"><thead><tr><th>Floor</th><th>Item in Chest</th></tr>'))
    e.set('floor', 10)
    while truth(binary('<', e['floor'], 121)):
        if truth(binary('>=', call(e['compareSemVer'], get(e['save'], 'version'), '1.6'), 0)):
            e.set('rng', call(e['CSRandom'], call(e['getRandomSeedFromBigInts'], call(get(call(e['bigInt'], get(e['save'], 'gameID')), 'times'), 512), call(e['bigInt'], e['floor']))))
        else:
            e.set('rng', call(e['CSRandom'], call(e['bigIntToSigned32'], call(get(call(get(call(e['bigInt'], get(e['save'], 'gameID')), 'times'), 512), 'plus'), e['floor']))))
        e.set('item', get(get(e['choices'], e['floor']), call(get(e['rng'], 'Next'), get(get(e['choices'], e['floor']), 'length'))))
        if truth(binary('!==', e['floor'], 30)):
            e.set('item', call(e['wikify'], e['item']))
        e.set('output', binary('+', e['output'], binary('+', binary('+', binary('+', binary('+', '<tr><td>', e['floor']), '</td><td>'), e['item']), '</tr></tr>')))
        e.set('floor', binary('+', e['floor'], 10))
    e.set('output', binary('+', e['output'], '</tbody></table>\n'))
    return e['output']
    return U


def predictGemBirds_225(parent, this, args):
    # Upstream predictor: 7641
    e = Env(parent)
    e.declare(['birds', 'gems', 'i', 'j', 'locs', 'output', 'rng', 'temp'])
    e.local['arguments'] = Array(args)
    e.local['isSearch'] = (args[0] if len(args) > 0 and args[0] is not U else U)
    e.local['offset'] = (args[1] if len(args) > 1 and args[1] is not U else U)
    e.set('output', '')
    e.set('birds', Array(['Green', 'Blue', 'Red', 'Purple', 'Brown']))
    e.set('gems', Obj({'Green': 'Emerald', 'Blue': 'Aquamarine', 'Red': 'Ruby', 'Purple': 'Amethyst', 'Brown': 'Topaz'}))
    e.set('locs', Array(['North (Dig Site / Volcano)', 'South (Docks / Resort)', 'East (Jungle)', 'West (Farm)']))
    if truth(binary('<', call(e['compareSemVer'], get(e['save'], 'version'), '1.5'), 0)):
        call(get(call(e['$'], '#gembirds-note'), 'html'), "This is meaningless in pre-1.5 games since the Island and birds don't exist.")
    else:
        call(get(call(e['$'], '#gembirds-note'), 'html'), '')
    e.set('output', binary('+', e['output'], '<table class="output"><thead><tr><th colspan>Direction (Location)</th><th>Bird Type</th></tr>'))
    if truth(binary('>=', call(e['compareSemVer'], get(e['save'], 'version'), '1.6'), 0)):
        e.set('rng', call(e['CSRandom'], call(e['getRandomSeed'], get(e['save'], 'gameID'))))
    else:
        e.set('rng', call(e['CSRandom'], get(e['save'], 'gameID')))
    e.set('i', get(e['birds'], 'length'))
    while truth(binary('>', e['i'], 1)):
        e.set('j', call(get(e['rng'], 'Next'), update_env(e, 'i', -1, False)))
        e.set('temp', get(e['birds'], e['i']))
        put(e['birds'], e['i'], get(e['birds'], e['j']))
        put(e['birds'], e['j'], e['temp'])
    e.set('i', 0)
    while truth(binary('<', e['i'], get(e['locs'], 'length'))):
        e.set('output', binary('+', e['output'], binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', '<tr><td>', get(e['locs'], e['i'])), '</td><td>'), get(e['birds'], e['i'])), ' ('), call(e['wikify'], get(e['gems'], get(e['birds'], e['i'])))), ')</td></tr>')))
        update_env(e, 'i', 1, False)
    e.set('output', binary('+', e['output'], '</tbody></table>\n'))
    return e['output']
    return U


def callback_240(parent, this, args):
    # Upstream predictor: 7812
    e = Env(parent)
    e.declare([])
    e.local['arguments'] = Array(args)
    e.local['i'] = (args[0] if len(args) > 0 and args[0] is not U else U)
    return call(e['wikify'], e['i'])
    return U


def callback_241(parent, this, args):
    # Upstream predictor: 7814
    e = Env(parent)
    e.declare([])
    e.local['arguments'] = Array(args)
    e.local['i'] = (args[0] if len(args) > 0 and args[0] is not U else U)
    return call(e['wikify'], e['i'])
    return U


def predictWinterStar_226(parent, this, args):
    # Upstream predictor: 7680
    e = Env(parent)
    e.declare(['UMP_ID', 'base', 'excluded', 'forceOldLogic', 'giftChoices', 'gifts', 'index', 'npcs', 'numPlayers', 'orig', 'output', 'pick', 'player', 'playerName', 'rng', 'secretSantaGetFrom', 'secretSantaGiveTo', 'seed', 'tclass', 'year'])
    e.local['arguments'] = Array(args)
    e.local['isSearch'] = (args[0] if len(args) > 0 and args[0] is not U else U)
    e.local['offset'] = (args[1] if len(args) > 1 and args[1] is not U else U)
    e.set('output', '')
    e.set('npcs', table(15))
    e.set('giftChoices', table(16))
    e.set('gifts', '')
    e.set('excluded', Obj({'Wizard': 1, 'Krobus': 1, 'Sandy': 1, 'Dwarf': 1, 'Marlon': 1}))
    e.set('secretSantaGiveTo', '')
    e.set('secretSantaGetFrom', '')
    e.set('numPlayers', 1)
    e.set('playerName', 'Farmer')
    e.set('forceOldLogic', False)
    if truth(binary('>=', call(e['compareSemVer'], get(e['save'], 'version'), '1.5'), 0)):
        call(get(e['npcs'], 'push'), 'Leo')
        if truth(unary('!', get(e['save'], 'leoMoved'))):
            put(e['excluded'], 'Leo', 1)
    if truth(binary('===', unary('typeof', e['offset']), 'undefined')):
        e.set('offset', binary('-', get(e['save'], 'year'), 1))
    if truth(binary('<', e['offset'], 1)):
        call(get(call(e['$'], '#winterstar-prev'), 'prop'), 'disabled', True)
    else:
        call(get(call(e['$'], '#winterstar-prev'), 'val'), binary('-', e['offset'], 1))
        call(get(call(e['$'], '#winterstar-prev'), 'prop'), 'disabled', False)
    call(get(call(e['$'], '#winterstar-reset'), 'val'), 'reset')
    call(get(call(e['$'], '#winterstar-next'), 'val'), binary('+', e['offset'], 1))
    e.set('year', binary('+', e['offset'], 1))
    if truth((binary('!==', unary('typeof', get(e['save'], 'mp_ids')), 'undefined') if truth(_logic227 := binary('!==', unary('typeof', get(e['save'], 'names')), 'undefined')) else _logic227)):
        e.set('numPlayers', get(get(e['save'], 'names'), 'length'))
        call(get(call(e['$'], '#winterstar-note'), 'html'), '')
    else:
        e.set('forceOldLogic', True)
        call(get(call(e['$'], '#winterstar-note'), 'html'), 'Note: No players found; predictions will not be reliable for game version > 1.2')
    e.set('output', binary('+', e['output'], binary('+', binary('+', '<table class="output"><thead><tr><th colspan = "4">Year ', e['year']), '</th></tr>')))
    e.set('output', binary('+', e['output'], '<tr><th>Player</th><th>Player gives gift to</th><th>Player receives gift from</th><th class="long_list">Possible gifts received</th></tr></thead>\n<tbody>'))
    e.set('player', 0)
    while truth(binary('<', e['player'], e['numPlayers'])):
        if truth((_logic228 if truth(_logic228 := e['forceOldLogic']) else binary('<', call(e['compareSemVer'], get(e['save'], 'version'), '1.3'), 0))):
            e.set('rng', call(e['CSRandom'], binary('-', binary('/', get(e['save'], 'gameID'), 2), e['year'])))
        else:
            e.set('UMP_ID', call(e['bigIntToSigned32'], get(get(e['save'], 'mp_ids'), e['player'])))
            e.set('base', call(e['bigIntToSigned32'], call(get(call(e['bigInt'], get(e['save'], 'gameID')), 'divide'), 2)))
            e.set('seed', binary('^', binary('^', e['base'], e['year']), e['UMP_ID']))
            e.set('rng', call(e['CSRandom'], e['seed']))
            e.set('playerName', get(get(e['save'], 'names'), e['player']))
        if truth((binary('>=', call(e['compareSemVer'], get(e['save'], 'version'), '1.6'), 0) if truth(_logic229 := unary('!', e['forceOldLogic'])) else _logic229)):
            e.set('orig', table(17))
            if truth(get(e['save'], 'leoMoved')):
                call(get(e['orig'], 'push'), 'Leo')
            e.set('npcs', call(get(e['orig'], 'slice')))
            e.set('secretSantaGiveTo', '')
            e.set('rng', call(e['CSRandom'], call(e['getRandomSeedFromBigInts'], call(get(call(e['bigInt'], get(e['save'], 'gameID')), 'divide'), 2), call(e['bigInt'], e['year']), get(get(e['save'], 'mp_ids'), e['player']))))
            while truth(binary('===', e['secretSantaGiveTo'], '')):
                e.set('index', call(get(e['rng'], 'Next'), get(e['npcs'], 'length')))
                e.set('pick', get(e['npcs'], e['index']))
                if truth((_logic230 if truth(_logic230 := binary('===', e['pick'], 'Marlon')) else (binary('===', e['pick'], 'Kent') if truth(_logic231 := binary('===', e['year'], 1)) else _logic231))):
                    call(get(e['npcs'], 'splice'), e['index'], 1)
                else:
                    e.set('secretSantaGiveTo', e['pick'])
            e.set('npcs', call(get(e['orig'], 'slice')))
            e.set('secretSantaGetFrom', '')
            call(get(e['npcs'], 'splice'), call(get(e['npcs'], 'indexOf'), e['secretSantaGiveTo']), 1)
            e.set('rng', call(e['CSRandom'], call(e['getRandomSeedFromBigInts'], call(get(call(e['bigInt'], get(e['save'], 'gameID')), 'divide'), 2), call(e['bigInt'], e['year']), get(get(e['save'], 'mp_ids'), e['player']))))
            while truth(binary('===', e['secretSantaGetFrom'], '')):
                e.set('index', call(get(e['rng'], 'Next'), get(e['npcs'], 'length')))
                e.set('pick', get(e['npcs'], e['index']))
                if truth((_logic232 if truth(_logic232 := binary('===', e['pick'], 'Marlon')) else (binary('===', e['pick'], 'Kent') if truth(_logic233 := binary('===', e['year'], 1)) else _logic233))):
                    call(get(e['npcs'], 'splice'), e['index'], 1)
                else:
                    e.set('secretSantaGetFrom', e['pick'])
        else:
            e.set('secretSantaGiveTo', get(e['npcs'], call(get(e['rng'], 'Next'), get(e['npcs'], 'length'))))
            e.set('secretSantaGetFrom', '')
            while truth((_logic234 if truth(_logic234 := call(get(e['excluded'], 'hasOwnProperty'), e['secretSantaGiveTo'])) else (binary('===', e['secretSantaGiveTo'], 'Kent') if truth(_logic235 := binary('===', e['year'], 1)) else _logic235))):
                e.set('secretSantaGiveTo', get(e['npcs'], call(get(e['rng'], 'Next'), get(e['npcs'], 'length'))))
            while truth((_logic236 if truth(_logic236 := (_logic237 if truth(_logic237 := (_logic238 if truth(_logic238 := binary('===', e['secretSantaGetFrom'], '')) else binary('===', e['secretSantaGetFrom'], e['secretSantaGiveTo']))) else call(get(e['excluded'], 'hasOwnProperty'), e['secretSantaGetFrom']))) else (binary('===', e['secretSantaGetFrom'], 'Kent') if truth(_logic239 := binary('===', e['year'], 1)) else _logic239))):
                e.set('secretSantaGetFrom', get(e['npcs'], call(get(e['rng'], 'Next'), get(e['npcs'], 'length'))))
        if truth(binary('<', e['year'], get(e['save'], 'year'))):
            e.set('tclass', 'past')
        else:
            if truth(binary('===', e['year'], get(e['save'], 'year'))):
                e.set('tclass', 'current')
            else:
                e.set('tclass', 'future')
        if truth(call(get(e['giftChoices'], 'hasOwnProperty'), e['secretSantaGetFrom'])):
            e.set('gifts', call(get(call(get(call(get(get(e['giftChoices'], e['secretSantaGetFrom']), 'map'), Fn(callback_240, e)), 'sort')), 'join'), ', '))
        else:
            e.set('gifts', call(get(call(get(call(get(get(e['giftChoices'], 'DEFAULT'), 'map'), Fn(callback_241, e)), 'sort')), 'join'), ', '))
        e.set('output', binary('+', e['output'], binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', '<tr class="', e['tclass']), '"><td>'), e['playerName']), '</td><td>'), call(e['wikify'], e['secretSantaGiveTo'])), '</td><td>'), call(e['wikify'], e['secretSantaGetFrom'])), '</td><td class="long_list">'), e['gifts']), '</td></tr>\n')))
        update_env(e, 'player', 1, False)
    e.set('output', binary('+', e['output'], '</tbody></table>\n'))
    return e['output']
    return U


def getNicerOutfitDescription_242(parent, this, args):
    # Upstream predictor: 7823
    e = Env(parent)
    e.declare(['newstr', 'pieces', 'regexCap'])
    e.local['arguments'] = Array(args)
    e.local['str'] = (args[0] if len(args) > 0 and args[0] is not U else U)
    e.set('regexCap', Regex('[A-Z]', 'g'))
    e.set('newstr', call(get(e['str'], 'replace'), e['regexCap'], ' $&'))
    e.set('pieces', call(get(call(get(e['newstr'], 'trim')), 'split'), '_'))
    if truth(binary('===', get(e['pieces'], 0), 'None')):
        put(e['pieces'], 0, '(No Hat)')
    return call(get(e['pieces'], 'join'), '<br/>')
    return U


def callback_246(parent, this, args):
    # Upstream predictor: 7915
    e = Env(parent)
    e.declare(['d'])
    e.local['arguments'] = Array(args)
    e.local['key'] = (args[0] if len(args) > 0 and args[0] is not U else U)
    e.local['index'] = (args[1] if len(args) > 1 and args[1] is not U else U)
    e.set('output', binary('+', e['output'], binary('+', binary('+', binary('+', binary('+', '<tr class="', e['tclass']), '"><td>Shop Vendor '), e['key']), '</td>')))
    e.set('d', 0)
    while truth(binary('<', e['d'], 3)):
        e.set('output', binary('+', e['output'], binary('+', binary('+', '<td>', call(e['wikify'], get(get(e['vendor'], e['key']), e['d']))), '</td>')))
        update_env(e, 'd', 1, False)
    e.set('output', binary('+', e['output'], '</tr>'))
    return U


def predictMakeover_243(parent, this, args):
    # Upstream predictor: 7835
    e = Env(parent)
    e.declare(['c', 'd', 'day', 'i', 'index', 'k', 'm', 'makeoverChoices', 'outfit', 'output', 'parts', 'player', 'possibleVendors', 'racerNames', 'racerPool', 'racers', 'rng', 'roll', 'scheduleExclusion', 'seed', 'tclass', 'umid', 'vendor', 'vendorPool', 'year'])
    e.local['arguments'] = Array(args)
    e.local['isSearch'] = (args[0] if len(args) > 0 and args[0] is not U else U)
    e.local['offset'] = (args[1] if len(args) > 1 and args[1] is not U else U)
    e.set('output', '')
    e.set('makeoverChoices', table(18))
    e.set('possibleVendors', table(19))
    e.set('scheduleExclusion', table(20))
    e.set('racerNames', Array(['Speed Rooster', 'King Sting', 'Shoebiscuit', 'Escar-go', 'Cactus Crawler']))
    if truth(binary('===', unary('typeof', e['offset']), 'undefined')):
        e.set('offset', binary('-', get(e['save'], 'year'), 1))
    if truth(binary('<', e['offset'], 1)):
        call(get(call(e['$'], '#makeover-prev'), 'prop'), 'disabled', True)
    else:
        call(get(call(e['$'], '#makeover-prev'), 'val'), binary('-', e['offset'], 1))
        call(get(call(e['$'], '#makeover-prev'), 'prop'), 'disabled', False)
    call(get(call(e['$'], '#makeover-reset'), 'val'), 'reset')
    call(get(call(e['$'], '#makeover-next'), 'val'), binary('+', e['offset'], 1))
    e.set('year', binary('+', e['offset'], 1))
    if truth(binary('<', e['year'], get(e['save'], 'year'))):
        e.set('tclass', 'past')
    else:
        if truth(binary('===', e['year'], get(e['save'], 'year'))):
            e.set('tclass', 'current')
        else:
            e.set('tclass', 'future')
    e.set('output', binary('+', e['output'], binary('+', binary('+', '<table class="output"><thead><tr><th colspan = "4">Year ', e['year']), '</th></tr>')))
    e.set('output', binary('+', e['output'], '<tr><th> </th><th>Monday Spring 15</th><th>Tuesday Spring 16</th><th>Wednesday Spring 17</th></tr></thead>\n<tbody>'))
    e.set('vendor', Obj({'1': Array([]), '2': Array([])}))
    e.set('racers', Obj({'0': Array([]), '1': Array([]), '2': Array([])}))
    e.set('d', 0)
    while truth(binary('<', e['d'], 3)):
        e.set('day', binary('+', binary('+', binary('*', 112, e['offset']), 15), e['d']))
        e.set('vendorPool', Array([]))
        e.set('c', 0)
        while truth(binary('<', e['c'], get(get(e['save'], 'characters'), 'length'))):
            if truth(unary('!', call(get(e['possibleVendors'], 'hasOwnProperty'), get(get(e['save'], 'characters'), e['c'])))):
                update_env(e, 'c', 1, False)
                continue
            if truth((binary('<', e['year'], 2) if truth(_logic244 := binary('===', get(get(e['save'], 'characters'), e['c']), 'Kent')) else _logic244)):
                update_env(e, 'c', 1, False)
                continue
            if truth((unary('!', get(e['save'], 'leoMoved')) if truth(_logic245 := binary('===', get(get(e['save'], 'characters'), e['c']), 'Leo')) else _logic245)):
                update_env(e, 'c', 1, False)
                continue
            if truth(call(get(get(e['scheduleExclusion'], e['d']), 'hasOwnProperty'), get(get(e['save'], 'characters'), e['c']))):
                update_env(e, 'c', 1, False)
                continue
            call(get(e['vendorPool'], 'push'), get(get(e['save'], 'characters'), e['c']))
            update_env(e, 'c', 1, False)
        e.set('rng', call(e['CSRandom'], call(e['getRandomSeed'], e['day'], binary('/', get(e['save'], 'gameID'), 2))))
        e.set('k', 0)
        while truth(binary('<', e['k'], e['d'])):
            e.set('m', 0)
            while truth(binary('<', e['m'], 2)):
                e.set('index', call(get(e['rng'], 'Next'), get(e['vendorPool'], 'length')))
                call(get(e['vendorPool'], 'splice'), e['index'], 1)
                update_env(e, 'm', 1, False)
            update_env(e, 'k', 1, False)
        e.set('i', 1)
        while truth(binary('<=', e['i'], 2)):
            e.set('index', call(get(e['rng'], 'Next'), get(e['vendorPool'], 'length')))
            call(get(get(e['vendor'], e['i']), 'push'), get(e['vendorPool'], e['index']))
            call(get(e['vendorPool'], 'splice'), e['index'], 1)
            update_env(e, 'i', 1, False)
        e.set('racerPool', Array([0, 1, 2, 3, 4]))
        e.set('i', 0)
        while truth(binary('<', e['i'], 3)):
            e.set('index', call(get(e['rng'], 'Next'), get(e['racerPool'], 'length')))
            call(get(get(e['racers'], e['d']), 'push'), get(e['racerNames'], get(e['racerPool'], e['index'])))
            call(get(e['racerPool'], 'splice'), e['index'], 1)
            update_env(e, 'i', 1, False)
        update_env(e, 'd', 1, False)
    call(get(call(get(call(get(e['Object'], 'keys'), e['vendor']), 'sort')), 'forEach'), Fn(callback_246, e))
    e.set('output', binary('+', e['output'], binary('+', binary('+', '<tr class="', e['tclass']), '"><td>Racers</td>')))
    e.set('d', 0)
    while truth(binary('<', e['d'], 3)):
        e.set('output', binary('+', e['output'], binary('+', binary('+', '<td>', call(get(get(e['racers'], e['d']), 'join'), '<br/>')), '</td>')))
        update_env(e, 'd', 1, False)
    e.set('output', binary('+', e['output'], '</tr>'))
    if truth((binary('>', get(get(e['save'], 'mp_ids'), 'length'), 0) if truth(_logic247 := binary('!==', unary('typeof', get(e['save'], 'mp_ids')), 'undefined')) else _logic247)):
        if truth(binary('===', get(get(e['save'], 'gender'), 0), '')):
            e.set('player', 0)
            while truth(binary('<', e['player'], get(get(e['save'], 'mp_ids'), 'length'))):
                put(get(e['save'], 'gender'), e['player'], 'Female')
                update_env(e, 'player', 1, False)
            call(get(call(e['$'], '#makeover-note'), 'html'), 'Warning: Predictor could not determing player gender. All players will be assumed to be female. To get better makeover predictions, use a game saved under current version.')
        e.set('player', 0)
        while truth(binary('<', e['player'], get(get(e['save'], 'mp_ids'), 'length'))):
            e.set('seed', call(e['bigIntToSigned32'], call(get(get(get(e['save'], 'mp_ids'), e['player']), 'add'), e['year'])))
            e.set('rng', call(e['CSRandom'], call(e['getRandomSeed'], e['seed'])))
            e.set('output', binary('+', e['output'], binary('+', binary('+', binary('+', binary('+', '<tr class="', e['tclass']), '"><td>Free "Cactis" for<br/>'), get(get(e['save'], 'names'), e['player'])), '</td>')))
            e.set('parts', Array([call(get(e['rng'], 'Next'), 24), call(get(e['rng'], 'Next'), 24), call(get(e['rng'], 'Next'), 16)]))
            e.set('output', binary('+', e['output'], binary('+', binary('+', '<td colspan="3"><img src="blank.png" class="cactis" id="c_top_', get(e['parts'], 0)), '" alt="Cactis Top"><br/>')))
            e.set('output', binary('+', e['output'], binary('+', binary('+', '<img src="blank.png" class="cactis" id="c_mid_', get(e['parts'], 1)), '" alt="Cactis Top"><br/>')))
            e.set('output', binary('+', e['output'], binary('+', binary('+', '<img src="blank.png" class="cactis" id="c_bot_', get(e['parts'], 2)), '" alt="Cactis Top"></td></tr>')))
            update_env(e, 'player', 1, False)
        e.set('player', 0)
        while truth(binary('<', e['player'], get(get(e['save'], 'mp_ids'), 'length'))):
            e.set('outfit', Obj({}))
            e.set('d', 0)
            while truth(binary('<', e['d'], 3)):
                e.set('day', binary('+', binary('+', binary('*', 112, e['offset']), 15), e['d']))
                e.set('rng', call(e['CSRandom'], call(e['getRandomSeed'], e['day'], binary('/', get(e['save'], 'gameID'), 2), e['year'])))
                if truth(binary('<', call(get(e['rng'], 'NextDouble')), 0.75)):
                    e.set('umid', call(e['bigIntToSigned32'], get(get(e['save'], 'mp_ids'), e['player'])))
                    e.set('rng', call(e['CSRandom'], call(e['getRandomSeed'], e['day'], binary('/', get(e['save'], 'gameID'), 2), e['year'], e['umid'])))
                e.set('roll', call(get(e['rng'], 'NextDouble')))
                put(e['outfit'], e['d'], get(get(e['makeoverChoices'], get(get(e['save'], 'gender'), e['player'])), call(get(e['Math'], 'floor'), binary('*', e['roll'], get(get(e['makeoverChoices'], get(get(e['save'], 'gender'), e['player'])), 'length')))))
                if truth(binary('===', e['d'], 1)):
                    e.set('rng', call(e['CSRandom'], call(e['getRandomSeed'], e['day'], binary('/', get(e['save'], 'gameID'), 2))))
                    if truth(binary('<', call(get(e['rng'], 'NextDouble')), 0.03)):
                        put(e['outfit'], e['d'], 'Laurel Wreath Crown<br/>Toga Shirt<br/>Skirt <span class="swatch" style="color:#f7f5cd">██</span>')
                update_env(e, 'd', 1, False)
            e.set('output', binary('+', e['output'], binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', '<tr class="', e['tclass']), '"><td>Makeover Outfit for<br/>'), get(get(e['save'], 'names'), e['player'])), '<br/>('), get(get(e['save'], 'gender'), e['player'])), ')</td>')))
            e.set('d', 0)
            while truth(binary('<', e['d'], 3)):
                e.set('output', binary('+', e['output'], binary('+', binary('+', '<td>', get(e['outfit'], e['d'])), '</td>')))
                update_env(e, 'd', 1, False)
            e.set('output', binary('+', e['output'], '</tr>'))
            update_env(e, 'player', 1, False)
    else:
        call(get(call(e['$'], '#makeover-note'), 'html'), 'Note: No players found; vendor predictions will probably not be reliable, cactis predictions cannot be made, and makeover predictions can only show generic results')
        e.set('output', binary('+', e['output'], binary('+', binary('+', '<tr class="', e['tclass']), '"><td>Free "Cactis"</td><td colspan="3">Cannot predict; no players found</td></tr>')))
        e.set('outfit', Array([Array([]), Array([])]))
        e.set('d', 0)
        while truth(binary('<', e['d'], 3)):
            e.set('day', binary('+', binary('+', binary('*', 112, e['offset']), 15), e['d']))
            e.set('rng', call(e['CSRandom'], call(e['getRandomSeed'], e['day'], binary('/', get(e['save'], 'gameID'), 2), e['year'])))
            call(get(e['rng'], 'NextDouble'))
            e.set('roll', call(get(e['rng'], 'NextDouble')))
            put(get(e['outfit'], 0), e['d'], get(get(e['makeoverChoices'], 'Female'), call(get(e['Math'], 'floor'), binary('*', e['roll'], get(get(e['makeoverChoices'], 'Female'), 'length')))))
            put(get(e['outfit'], 1), e['d'], get(get(e['makeoverChoices'], 'Male'), call(get(e['Math'], 'floor'), binary('*', e['roll'], get(get(e['makeoverChoices'], 'Male'), 'length')))))
            if truth(binary('===', e['d'], 1)):
                e.set('rng', call(e['CSRandom'], call(e['getRandomSeed'], e['day'], binary('/', get(e['save'], 'gameID'), 2))))
                if truth(binary('<', call(get(e['rng'], 'NextDouble')), 0.03)):
                    put(get(e['outfit'], 0), e['d'], 'Laurel Wreath Crown<br/>Toga Shirt<br/>Skirt <span class="swatch" style="color:#f7f5cd">██</span>')
                    put(get(e['outfit'], 1), e['d'], 'Laurel Wreath Crown<br/>Toga Shirt<br/>Skirt <span class="swatch" style="color:#f7f5cd">██</span>')
            update_env(e, 'd', 1, False)
        e.set('output', binary('+', e['output'], binary('+', binary('+', '<tr class="', e['tclass']), '"><td>Makeover Outfit for<br/>Generic Female Player</td>')))
        e.set('d', 0)
        while truth(binary('<', e['d'], 3)):
            e.set('output', binary('+', e['output'], binary('+', binary('+', '<td>', get(get(e['outfit'], 0), e['d'])), '</td>')))
            update_env(e, 'd', 1, False)
        e.set('output', binary('+', e['output'], '</tr>'))
        e.set('output', binary('+', e['output'], binary('+', binary('+', '<tr class="', e['tclass']), '"><td>Makeover Outfit for<br/>Generic Male Player</td>')))
        e.set('d', 0)
        while truth(binary('<', e['d'], 3)):
            e.set('output', binary('+', e['output'], binary('+', binary('+', '<td>', get(get(e['outfit'], 1), e['d'])), '</td>')))
            update_env(e, 'd', 1, False)
        e.set('output', binary('+', e['output'], '</tr>'))
    e.set('output', binary('+', e['output'], '</tbody></table>\n'))
    return e['output']
    return U


def predictGreenRain_248(parent, this, args):
    # Upstream predictor: 8002
    e = Env(parent)
    e.declare(['day', 'dayOfMonth', 'festivalDays', 'grDays', 'greenRainDay', 'icon', 'month', 'monthName', 'output', 'rainChance', 'rng', 'season', 'tclass', 'weatherTown', 'week', 'weekDay', 'year'])
    e.local['arguments'] = Array(args)
    e.local['isSearch'] = (args[0] if len(args) > 0 and args[0] is not U else U)
    e.local['offset'] = (args[1] if len(args) > 1 and args[1] is not U else U)
    e.set('output', '')
    e.set('grDays', Array([5, 6, 7, 14, 15, 16, 18, 23]))
    e.set('festivalDays', table(21))
    if truth(binary('===', unary('typeof', e['offset']), 'undefined')):
        e.set('offset', binary('*', 28, call(get(e['Math'], 'floor'), binary('/', get(e['save'], 'daysPlayed'), 28))))
    if truth(binary('<', e['offset'], 112)):
        call(get(call(e['$'], '#greenrain-prev-year'), 'prop'), 'disabled', True)
    else:
        call(get(call(e['$'], '#greenrain-prev-year'), 'val'), binary('-', e['offset'], 112))
        call(get(call(e['$'], '#greenrain-prev-year'), 'prop'), 'disabled', False)
    if truth(binary('<', e['offset'], 28)):
        call(get(call(e['$'], '#greenrain-prev-month'), 'prop'), 'disabled', True)
    else:
        call(get(call(e['$'], '#greenrain-prev-month'), 'val'), binary('-', e['offset'], 28))
        call(get(call(e['$'], '#greenrain-prev-month'), 'prop'), 'disabled', False)
    call(get(call(e['$'], '#greenrain-reset'), 'val'), 'reset')
    call(get(call(e['$'], '#greenrain-next-month'), 'val'), binary('+', e['offset'], 28))
    call(get(call(e['$'], '#greenrain-next-year'), 'val'), binary('+', e['offset'], 112))
    e.set('month', call(get(e['Math'], 'floor'), binary('/', e['offset'], 28)))
    e.set('season', binary('%', e['month'], 4))
    e.set('monthName', get(get(e['save'], 'seasonNames'), e['season']))
    e.set('year', binary('+', 1, call(get(e['Math'], 'floor'), binary('/', e['offset'], 112))))
    e.set('rng', call(e['CSRandom'], call(e['getRandomSeed'], binary('*', e['year'], 777), get(e['save'], 'gameID'))))
    e.set('greenRainDay', get(e['grDays'], call(get(e['rng'], 'Next'), get(e['grDays'], 'length'))))
    e.set('output', binary('+', e['output'], binary('+', binary('+', binary('+', binary('+', '<table class="calendar"><thead><tr><th colspan="7">', e['monthName']), ' Year '), e['year']), '</th></tr>\n')))
    e.set('output', binary('+', e['output'], '<tr><th>M</th><th>T</th><th>W</th><th>Th</th><th>F</th><th>Sa</th><th>Su</th></tr></thead>\n<tbody>'))
    e.set('week', 0)
    while truth(binary('<', e['week'], 4)):
        e.set('output', binary('+', e['output'], '<tr>'))
        e.set('weekDay', 1)
        while truth(binary('<', e['weekDay'], 8)):
            e.set('day', binary('+', binary('+', binary('*', 7, e['week']), e['weekDay']), e['offset']))
            e.set('weatherTown', 'Sun')
            if truth((_logic249 if truth(_logic249 := (_logic250 if truth(_logic250 := (_logic251 if truth(_logic251 := binary('==', e['day'], 1)) else binary('==', e['day'], 2))) else binary('==', e['day'], 4))) else binary('==', binary('%', e['day'], 28), 1))):
                e.set('weatherTown', 'Sun')
            else:
                if truth(binary('==', e['day'], 3)):
                    e.set('weatherTown', 'Rain')
                else:
                    if truth(call(get(e['festivalDays'], 'hasOwnProperty'), binary('%', e['day'], 112))):
                        e.set('weatherTown', get(e['festivalDays'], binary('%', e['day'], 112)))
                    else:
                        _switch252 = e['season']
                        _switch252_index = -1
                        if _switch252_index < 0 and strict_equal(_switch252, 0): _switch252_index = 0
                        if _switch252_index < 0 and strict_equal(_switch252, 2): _switch252_index = 1
                        if _switch252_index < 0 and strict_equal(_switch252, 1): _switch252_index = 2
                        if _switch252_index < 0: _switch252_index = -1
                        while True:
                            if 0 <= _switch252_index <= 0:
                                pass
                            if 0 <= _switch252_index <= 1:
                                e.set('rng', call(e['CSRandom'], call(e['getRandomSeed'], call(e['getHashFromString'], 'location_weather'), get(e['save'], 'gameID'), binary('-', e['day'], 1))))
                                if truth(binary('<', call(get(e['rng'], 'NextDouble')), 0.183)):
                                    e.set('weatherTown', 'Rain')
                                break
                            if 0 <= _switch252_index <= 2:
                                e.set('dayOfMonth', binary('-', binary('%', e['day'], 112), 28))
                                e.set('rng', call(e['CSRandom'], call(e['getRandomSeed'], binary('-', e['day'], 1), binary('/', get(e['save'], 'gameID'), 2), call(e['getHashFromString'], 'summer_rain_chance'))))
                                if truth(binary('==', e['dayOfMonth'], e['greenRainDay'])):
                                    e.set('weatherTown', 'Green Rain')
                                else:
                                    if truth(binary('==', binary('%', e['dayOfMonth'], 13), 0)):
                                        e.set('weatherTown', 'Storm')
                                    else:
                                        e.set('rainChance', binary('+', 0.12, binary('*', 0.003, binary('-', e['dayOfMonth'], 1))))
                                        if truth(binary('<', call(get(e['rng'], 'NextDouble')), e['rainChance'])):
                                            e.set('weatherTown', 'Rain')
                                break
                            break
            if truth(binary('<', e['day'], get(e['save'], 'daysPlayed'))):
                e.set('tclass', 'past')
            else:
                if truth(binary('===', e['day'], get(e['save'], 'daysPlayed'))):
                    e.set('tclass', 'current')
                else:
                    e.set('tclass', 'future')
            e.set('icon', ('<img src="blank.png" class="icon" alt="Clear" id="w_rain">' if truth((_logic253 if truth(_logic253 := (_logic254 if truth(_logic254 := binary('==', e['weatherTown'], 'Rain')) else binary('==', e['weatherTown'], 'Green Rain'))) else binary('==', e['weatherTown'], 'Storm'))) else '<img src="blank.png" class="icon" alt="Umbrella in rain" id="w_sun">'))
            e.set('output', binary('+', e['output'], binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', '<td class="', e['tclass']), '"><span class="date"> '), binary('-', e['day'], e['offset'])), '</span><br/>'), '<span class="cell">'), e['icon']), e['weatherTown']), '</span></td>')))
            update_env(e, 'weekDay', 1, False)
        e.set('output', binary('+', e['output'], '</tr>\n'))
        update_env(e, 'week', 1, False)
    e.set('output', binary('+', e['output'], '<tr><td colspan="7" class="legend"><img src="blank.png" class="icon" alt="Umbrella in rain" id="w_rain"> Rainy weather. "Rain" could become Storm.<br/><img src="blank.png" class="icon" alt="Shining Sun" id="w_sun"> Clear weather. "Sun" could become Wind or Snow.</td></tr>'))
    e.set('output', binary('+', e['output'], '</tbody></table>\n'))
    return e['output']
    return U


def predictCalicoJack_255(parent, this, args):
    # Upstream predictor: 8113
    e = Env(parent)
    e.declare(['advice', 'autoBust', 'c', 'c1', 'c2', 'chance', 'choice', 'count', 'dayOfMonth', 'dayOfWeek', 'dealerStart', 'dealerTotal', 'distance', 'g', 'havePush', 'hit', 'i', 'minRoll', 'month', 'monthName', 'next', 'numPlayed', 'output', 'pageSize', 'playerTotal', 'r', 'rng', 'roll', 'sbRoll', 'startHand', 'superBust', 'tclass', 'year'])
    e.local['arguments'] = Array(args)
    e.local['isSearch'] = (args[0] if len(args) > 0 and args[0] is not U else U)
    e.local['offset'] = (args[1] if len(args) > 1 and args[1] is not U else U)
    e.local['gameOffset'] = (args[2] if len(args) > 2 and args[2] is not U else 0)
    e.set('output', '')
    e.set('pageSize', 20)
    if truth((binary('!==', e['offset'], '') if truth(_logic256 := (binary('!==', unary('typeof', e['offset']), 'undefined') if truth(_logic257 := e['isSearch']) else _logic257)) else _logic256)):
        pass
    else:
        if truth(binary('===', unary('typeof', e['offset']), 'undefined')):
            e.set('offset', binary('+', get(e['save'], 'daysPlayed'), get(e['save'], 'dayAdjust')))
        call(get(call(e['$'], '#cj-d-next-week'), 'val'), binary('+', e['offset'], 7))
        call(get(call(e['$'], '#cj-d-prev-week'), 'val'), binary('-', e['offset'], 7))
        call(get(call(e['$'], '#cj-d-next-day'), 'val'), binary('+', e['offset'], 1))
        call(get(call(e['$'], '#cj-d-prev-day'), 'val'), binary('-', e['offset'], 1))
        if truth(binary('<', e['offset'], 7)):
            call(get(call(e['$'], '#cj-d-prev-week'), 'prop'), 'disabled', True)
        else:
            call(get(call(e['$'], '#cj-d-prev-week'), 'prop'), 'disabled', False)
        if truth(binary('<', e['offset'], 2)):
            call(get(call(e['$'], '#cj-d-prev-day'), 'prop'), 'disabled', True)
        else:
            call(get(call(e['$'], '#cj-d-prev-day'), 'prop'), 'disabled', False)
        call(get(call(e['$'], '#cj-d-reset'), 'val'), 'reset')
        call(get(call(e['$'], '#cj-d-next-week'), 'prop'), 'disabled', False)
        call(get(call(e['$'], '#cj-d-next-day'), 'prop'), 'disabled', False)
        if truth(binary('<', e['gameOffset'], e['pageSize'])):
            call(get(call(e['$'], '#cj-g-prev'), 'prop'), 'disabled', True)
        else:
            call(get(call(e['$'], '#cj-g-prev'), 'val'), binary('-', e['gameOffset'], e['pageSize']))
            call(get(call(e['$'], '#cj-g-prev'), 'prop'), 'disabled', False)
        if truth(binary('<', e['gameOffset'], 100)):
            call(get(call(e['$'], '#cj-g-prev-100'), 'prop'), 'disabled', True)
        else:
            call(get(call(e['$'], '#cj-g-prev-100'), 'val'), binary('-', e['gameOffset'], 100))
            call(get(call(e['$'], '#cj-g-prev-100'), 'prop'), 'disabled', False)
        call(get(call(e['$'], '#cj-g-reset'), 'val'), 'reset')
        call(get(call(e['$'], '#cj-g-next'), 'val'), binary('+', e['gameOffset'], e['pageSize']))
        call(get(call(e['$'], '#cj-g-next'), 'prop'), 'disabled', False)
        call(get(call(e['$'], '#cj-g-next-100'), 'val'), binary('+', e['gameOffset'], 100))
        call(get(call(e['$'], '#cj-g-next-100'), 'prop'), 'disabled', False)
        e.set('dayOfMonth', binary('%', e['offset'], 28))
        e.set('dayOfWeek', binary('%', binary('-', e['offset'], 1), 7))
        if truth(binary('!==', e['dayOfMonth'], 0)):
            e.set('month', call(get(e['Math'], 'floor'), binary('/', e['offset'], 28)))
            e.set('year', binary('+', 1, call(get(e['Math'], 'floor'), binary('/', e['offset'], 112))))
        else:
            e.set('dayOfMonth', 28)
            e.set('month', binary('-', call(get(e['Math'], 'floor'), binary('/', e['offset'], 28)), 1))
            e.set('monthName', get(get(e['save'], 'seasonNames'), binary('%', e['month'], 4)))
            e.set('year', binary('+', 1, call(get(e['Math'], 'floor'), binary('/', binary('-', e['offset'], 1), 112))))
        e.set('monthName', get(get(e['save'], 'seasonNames'), binary('%', e['month'], 4)))
        e.set('output', binary('+', e['output'], binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', '<table class="output"><thead><tr><th class="index" rowspan="2">Game<br/>Count</th>', '<th class="cj-result" colspan="2">'), get(get(e['save'], 'dayNames'), e['dayOfWeek'])), ' '), e['monthName']), ' '), e['dayOfMonth']), ', Year '), e['year']), '</th></tr>')))
        e.set('output', binary('+', e['output'], '<tr><th>Starting Hand</th><th>Best Strategy</th></tr></thead><tbody>'))
        e.set('g', 1)
        while truth(binary('<=', e['g'], e['pageSize'])):
            e.set('numPlayed', binary('+', e['gameOffset'], e['g']))
            e.set('advice', 'LOSS (Unavoidable)')
            if truth(binary('>=', call(e['compareSemVer'], get(e['save'], 'version'), '1.6'), 0)):
                e.set('rng', call(e['CSRandom'], call(e['getRandomSeed'], e['numPlayed'], e['offset'], get(e['save'], 'gameID'))))
            else:
                e.set('rng', call(e['CSRandom'], binary('+', binary('+', e['numPlayed'], e['offset']), get(e['save'], 'gameID'))))
            e.set('dealerStart', binary('+', call(get(e['rng'], 'Next'), 1, 12), call(get(e['rng'], 'Next'), 1, 10)))
            e.set('c1', call(get(e['rng'], 'Next'), 1, 12))
            e.set('c2', call(get(e['rng'], 'Next'), 1, 10))
            e.set('startHand', binary('+', binary('+', binary('+', '', e['c1']), ' and '), e['c2']))
            e.set('playerTotal', binary('+', e['c1'], e['c2']))
            e.set('roll', Array([]))
            e.set('i', 0)
            while truth(binary('<', e['i'], 60)):
                put(e['roll'], e['i'], call(get(e['rng'], 'NextDouble')))
                update_env(e, 'i', 1, False)
            e.set('r', 0)
            e.set('hit', 0)
            e.set('choice', Array([]))
            while truth(binary('<', e['playerTotal'], 21)):
                call(get(e['choice'], 'push'), Obj({'t': e['playerTotal'], 'r': e['r'], 'h': update_env(e, 'hit', 1, False)}))
                e.set('next', call(get(e['Math'], 'floor'), binary('+', binary('*', 9, get(e['roll'], update_env(e, 'r', 1, False))), 1)))
                e.set('distance', binary('-', 21, e['playerTotal']))
                if truth((binary('<', get(e['roll'], update_env(e, 'r', 1, False)), binary('/', 1, e['distance'])) if truth(_logic258 := (binary('<', e['distance'], 6) if truth(_logic259 := binary('>', e['distance'], 1)) else _logic259)) else _logic258)):
                    e.set('next', (e['distance'] if truth(binary('<', get(e['roll'], update_env(e, 'r', 1, False)), 0.5)) else binary('-', e['distance'], 1)))
                e.set('playerTotal', binary('+', e['playerTotal'], e['next']))
            if truth(binary('===', e['playerTotal'], 21)):
                e.set('advice', binary('+', binary('+', binary('+', binary('+', 'WIN: Hit ', e['hit']), ' time'), ('' if truth(binary('==', e['hit'], 1)) else 's')), ' to reach 21'))
            else:
                e.set('havePush', False)
                e.set('i', 0)
                while truth(binary('<', e['i'], get(e['choice'], 'length'))):
                    e.set('playerTotal', get(get(e['choice'], e['i']), 't'))
                    e.set('r', get(get(e['choice'], e['i']), 'r'))
                    e.set('dealerTotal', e['dealerStart'])
                    e.set('superBust', '')
                    while truth((_logic260 if truth(_logic260 := binary('<', e['dealerTotal'], 18)) else binary('<', e['dealerTotal'], e['playerTotal']))):
                        e.set('next', call(get(e['Math'], 'floor'), binary('+', binary('*', 9, get(e['roll'], update_env(e, 'r', 1, False))), 1)))
                        e.set('distance', binary('-', 21, e['dealerTotal']))
                        e.set('autoBust', False)
                        _switch261 = e['playerTotal']
                        _switch261_index = -1
                        if _switch261_index < 0 and strict_equal(_switch261, 20): _switch261_index = 0
                        if _switch261_index < 0 and strict_equal(_switch261, 19): _switch261_index = 1
                        if _switch261_index < 0 and strict_equal(_switch261, 18): _switch261_index = 2
                        if _switch261_index < 0: _switch261_index = 3
                        while True:
                            if 0 <= _switch261_index <= 0:
                                e.set('autoBust', binary('<', get(e['roll'], update_env(e, 'r', 1, False)), 0.5))
                                break
                            if 0 <= _switch261_index <= 1:
                                e.set('autoBust', binary('<', get(e['roll'], update_env(e, 'r', 1, False)), 0.25))
                                break
                            if 0 <= _switch261_index <= 2:
                                e.set('autoBust', binary('<', get(e['roll'], update_env(e, 'r', 1, False)), 0.1))
                                break
                            if 0 <= _switch261_index <= 3:
                                pass
                            break
                        if truth(e['autoBust']):
                            e.set('next', call(get(e['Math'], 'floor'), binary('+', binary('+', e['distance'], binary('*', 3, get(e['roll'], update_env(e, 'r', 1, False)))), 1)))
                        e.set('minRoll', 0.0005)
                        e.set('chance', call(get(e['Math'], 'max'), 0.0005, binary('+', binary('+', 0.001, binary('/', get(e['save'], 'dailyLuck'), 20)), binary('*', get(e['save'], 'luckLevel'), 0.002))))
                        e.set('sbRoll', get(e['roll'], update_env(e, 'r', 1, False)))
                        if truth(binary('<', e['sbRoll'], e['minRoll'])):
                            e.set('next', 999)
                            e.set('superBust', '<br/>Guaranteed super bust with 3x winnings')
                        else:
                            if truth(binary('<', e['sbRoll'], e['chance'])):
                                e.set('next', 999)
                                e.set('superBust', '<br/>Probable super bust with 3x winnings')
                        e.set('dealerTotal', binary('+', e['dealerTotal'], e['next']))
                    if truth(binary('>', e['dealerTotal'], 21)):
                        if truth(binary('===', get(get(e['choice'], e['i']), 'h'), 0)):
                            e.set('advice', binary('+', 'WIN: Stand at initial ', e['playerTotal']))
                        else:
                            e.set('advice', binary('+', binary('+', binary('+', binary('+', binary('+', 'WIN: Hit ', get(get(e['choice'], e['i']), 'h')), ' time'), ('' if truth(binary('==', get(get(e['choice'], e['i']), 'h'), 1)) else 's')), ' and stand at '), e['playerTotal']))
                        break
                    else:
                        if truth((unary('!', e['havePush']) if truth(_logic262 := binary('==', e['dealerTotal'], e['playerTotal'])) else _logic262)):
                            e.set('havePush', True)
                            e.set('advice', binary('+', binary('+', binary('+', binary('+', binary('+', 'TIE: Hit ', get(get(e['choice'], e['i']), 'h')), ' time'), ('' if truth(binary('==', get(get(e['choice'], e['i']), 'h'), 1)) else 's')), ' and stand at '), e['playerTotal']))
                    e.set('advice', binary('+', e['advice'], e['superBust']))
                    update_env(e, 'i', 1, False)
            if truth(binary('===', e['offset'], binary('+', get(e['save'], 'daysPlayed'), get(e['save'], 'dayAdjust')))):
                e.set('tclass', 'current')
            else:
                if truth(binary('<=', e['offset'], binary('+', get(e['save'], 'daysPlayed'), get(e['save'], 'dayAdjust')))):
                    e.set('tclass', 'past')
                else:
                    e.set('tclass', 'future')
            e.set('output', binary('+', e['output'], binary('+', binary('+', binary('+', binary('+', '<tr class="', e['tclass']), '"><td>'), call(e['addCommas'], e['numPlayed'])), '</td>')))
            e.set('output', binary('+', e['output'], binary('+', binary('+', '<td>', e['startHand']), '</td>')))
            e.set('output', binary('+', e['output'], binary('+', binary('+', '<td class="long_list">', e['advice']), '</td></tr>')))
            update_env(e, 'g', 1, False)
    e.set('output', binary('+', e['output'], '</tbody></table>'))
    return e['output']
    return U


def callback_267(parent, this, args):
    # Upstream predictor: 8337
    e = Env(parent)
    e.declare([])
    e.local['arguments'] = Array(args)
    e.local['a'] = (args[0] if len(args) > 0 and args[0] is not U else U)
    e.local['b'] = (args[1] if len(args) > 1 and args[1] is not U else U)
    return binary('-', e['a'], e['b'])
    return U


def callback_271(parent, this, args):
    # Upstream predictor: 8423
    e = Env(parent)
    e.declare([])
    e.local['arguments'] = Array(args)
    e.local['a'] = (args[0] if len(args) > 0 and args[0] is not U else U)
    e.local['b'] = (args[1] if len(args) > 1 and args[1] is not U else U)
    return binary('-', e['a'], e['b'])
    return U


def predictBookseller_263(parent, this, args):
    # Upstream predictor: 8303
    e = Env(parent)
    e.declare(['booksLeft', 'count', 'd', 'dateString', 'dayOfWeek', 'days', 'daysPlayed', 'i', 'month', 'monthName', 'monthsPlayed', 'output', 'picked', 'possibleDays', 'randBookList', 'rng', 'rngSynced', 'searchEnd', 'searchStart', 'searchTerm', 'seasonIndex', 'skillBookList', 'stock', 'tclass', 'year'])
    e.local['arguments'] = Array(args)
    e.local['isSearch'] = (args[0] if len(args) > 0 and args[0] is not U else U)
    e.local['offset'] = (args[1] if len(args) > 1 and args[1] is not U else U)
    e.set('output', '')
    e.set('skillBookList', Array(['Stardew Valley Almanac', 'Bait And Bobber', "Woodcutter's Weekly", 'Mining Monthly', 'Combat Quarterly']))
    e.set('randBookList', table(22))
    if truth((binary('!==', e['offset'], '') if truth(_logic264 := (binary('!==', unary('typeof', e['offset']), 'undefined') if truth(_logic265 := e['isSearch']) else _logic265)) else _logic264)):
        call(get(call(e['$'], '#book-prev-year'), 'prop'), 'disabled', True)
        call(get(call(e['$'], '#book-prev-month'), 'prop'), 'disabled', True)
        call(get(call(e['$'], '#book-next-month'), 'prop'), 'disabled', True)
        call(get(call(e['$'], '#book-prev-year'), 'prop'), 'disabled', True)
        call(get(call(e['$'], '#book-reset'), 'html'), 'Clear Search Results &amp; Reset Browsing')
        e.set('searchTerm', call(e['RegExp'], e['offset'], 'i'))
        e.set('searchStart', (0 if truth(call(get(call(e['$'], '#book-search-all'), 'prop'), 'checked')) else binary('*', 7, call(get(e['Math'], 'floor'), binary('/', binary('-', get(e['save'], 'daysPlayed'), 1), 7)))))
        e.set('searchEnd', binary('*', 112, call(get(call(e['$'], '#book-search-range'), 'val'))))
        e.set('output', binary('+', e['output'], binary('+', binary('+', binary('+', binary('+', binary('+', '<table class="output"><thead><tr><th colspan="3">Search results for &quot;', e['offset']), '&quot; over the '), ('first ' if truth(call(get(call(e['$'], '#book-search-all'), 'prop'), 'checked')) else 'next ')), call(get(call(e['$'], '#book-search-range'), 'val'))), ' year(s)</th></tr>\n')))
        e.set('output', binary('+', e['output'], '<tr><th class="day">Day</th><th class="item">Item</th><th class="price">Price</th></tr>\n<tbody>'))
        e.set('count', 0)
        e.set('offset', e['searchStart'])
        while truth(binary('<', e['offset'], binary('+', e['searchStart'], e['searchEnd']))):
            e.set('month', call(get(e['Math'], 'floor'), binary('/', e['offset'], 28)))
            e.set('seasonIndex', binary('%', e['month'], 4))
            e.set('monthName', get(get(e['save'], 'seasonNames'), e['seasonIndex']))
            e.set('year', binary('+', 1, call(get(e['Math'], 'floor'), binary('/', e['offset'], 112))))
            e.set('rng', call(e['CSRandom'], call(e['getRandomSeed'], binary('*', e['year'], 11), get(e['save'], 'gameID'), e['seasonIndex'])))
            e.set('possibleDays', Array([]))
            _switch266 = e['seasonIndex']
            _switch266_index = -1
            if _switch266_index < 0 and strict_equal(_switch266, 0): _switch266_index = 0
            if _switch266_index < 0 and strict_equal(_switch266, 1): _switch266_index = 1
            if _switch266_index < 0 and strict_equal(_switch266, 2): _switch266_index = 2
            if _switch266_index < 0 and strict_equal(_switch266, 3): _switch266_index = 3
            if _switch266_index < 0: _switch266_index = -1
            while True:
                if 0 <= _switch266_index <= 0:
                    e.set('possibleDays', Array([11, 12, 21, 22, 25]))
                    break
                if 0 <= _switch266_index <= 1:
                    e.set('possibleDays', Array([9, 12, 18, 25, 27]))
                    break
                if 0 <= _switch266_index <= 2:
                    e.set('possibleDays', Array([4, 7, 8, 9, 12, 19, 22, 25]))
                    break
                if 0 <= _switch266_index <= 3:
                    e.set('possibleDays', Array([5, 11, 12, 19, 22, 24]))
                    break
                break
            e.set('i', call(get(e['rng'], 'Next'), get(e['possibleDays'], 'length')))
            e.set('days', Array([get(e['possibleDays'], e['i']), get(e['possibleDays'], call(get(e['Math'], 'floor'), binary('%', binary('+', e['i'], binary('/', get(e['possibleDays'], 'length'), 2)), get(e['possibleDays'], 'length'))))]))
            call(get(e['days'], 'sort'), Fn(callback_267, e))
            e.set('d', 0)
            while truth(binary('<', e['d'], get(e['days'], 'length'))):
                e.set('dayOfWeek', get(get(e['save'], 'dayNames'), binary('%', binary('+', 6, get(e['days'], e['d'])), 7)))
                e.set('daysPlayed', binary('+', binary('+', e['offset'], get(e['days'], e['d'])), get(e['save'], 'dayAdjust')))
                e.set('dateString', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', e['dayOfWeek'], ' '), e['monthName']), ' '), get(e['days'], e['d'])), ', Year '), e['year']))
                e.set('rng', call(e['CSRandom'], call(e['getRandomSeed'], e['daysPlayed'], binary('/', get(e['save'], 'gameID'), 2))))
                e.set('rngSynced', call(e['CSRandom'], call(e['getRandomSeed'], call(e['getHashFromString'], 'purplebookSale'), get(e['save'], 'gameID'), e['daysPlayed'])))
                if truth((binary('<', call(get(e['rngSynced'], 'NextDouble')), 0.25) if truth(_logic268 := call(get(e['searchTerm'], 'test'), 'Book Of Stars')) else _logic268)):
                    update_env(e, 'count', 1, False)
                    e.set('output', binary('+', e['output'], binary('+', binary('+', binary('+', binary('+', '<tr><td>', e['dateString']), '</td><td class="book">'), call(e['wikify'], 'Book Of Stars')), '</td><td>15,000g</td></tr>')))
                e.set('booksLeft', call(get(e['skillBookList'], 'slice')))
                e.set('rngSynced', call(e['CSRandom'], call(e['getRandomSeed'], call(e['getHashFromString'], 'thirdBookSale'), get(e['save'], 'gameID'), e['daysPlayed'])))
                if truth(binary('<', call(get(e['rngSynced'], 'NextDouble')), 0.6)):
                    e.set('picked', call(get(e['booksLeft'], 'splice'), call(get(e['rng'], 'Next'), get(e['booksLeft'], 'length')), 1))
                    if truth(call(get(e['searchTerm'], 'test'), get(e['picked'], 0))):
                        update_env(e, 'count', 1, False)
                        e.set('output', binary('+', e['output'], binary('+', binary('+', binary('+', binary('+', '<tr><td>', e['dateString']), '</td><td class="book">'), call(e['wikify'], get(e['picked'], 0))), '</td><td>10,000g</td></tr>')))
                e.set('rngSynced', call(e['CSRandom'], call(e['getRandomSeed'], call(e['getHashFromString'], 'secondBookSale'), get(e['save'], 'gameID'), e['daysPlayed'])))
                if truth(binary('<', call(get(e['rngSynced'], 'NextDouble')), 0.8)):
                    e.set('picked', call(get(e['booksLeft'], 'splice'), call(get(e['rng'], 'Next'), get(e['booksLeft'], 'length')), 1))
                    if truth(call(get(e['searchTerm'], 'test'), get(e['picked'], 0))):
                        update_env(e, 'count', 1, False)
                        e.set('output', binary('+', e['output'], binary('+', binary('+', binary('+', binary('+', '<tr><td>', e['dateString']), '</td><td class="book">'), call(e['wikify'], get(e['picked'], 0))), '</td><td>8,000g</td></tr>')))
                e.set('picked', call(get(e['booksLeft'], 'splice'), call(get(e['rng'], 'Next'), get(e['booksLeft'], 'length')), 1))
                if truth(call(get(e['searchTerm'], 'test'), get(e['picked'], 0))):
                    update_env(e, 'count', 1, False)
                    e.set('output', binary('+', e['output'], binary('+', binary('+', binary('+', binary('+', '<tr><td>', e['dateString']), '</td><td class="book">'), call(e['wikify'], get(e['picked'], 0))), '</td><td>5,000g</td></tr>')))
                if truth(binary('>=', e['year'], 3)):
                    e.set('picked', get(e['randBookList'], call(get(e['rng'], 'Next'), get(e['randBookList'], 'length'))))
                    if truth(call(get(e['searchTerm'], 'test'), e['picked'])):
                        update_env(e, 'count', 1, False)
                        e.set('output', binary('+', e['output'], binary('+', binary('+', binary('+', binary('+', '<tr><td>', e['dateString']), '</td><td class="book">'), call(e['wikify'], e['picked'])), '</td><td>20,000g</td></tr>')))
                e.set('rngSynced', call(e['CSRandom'], call(e['getRandomSeed'], call(e['getHashFromString'], 'bookExtraForaging'), get(e['save'], 'gameID'), e['daysPlayed'])))
                if truth((binary('<', call(get(e['rngSynced'], 'NextDouble')), 0.33) if truth(_logic269 := call(get(e['searchTerm'], 'test'), "Woodcutter's Weekly")) else _logic269)):
                    update_env(e, 'count', 1, False)
                    e.set('output', binary('+', e['output'], binary('+', binary('+', binary('+', binary('+', '<tr><td>', e['dateString']), '</td><td class="book">'), call(e['wikify'], "Woodcutter's Weekly")), '</td><td>8,000g</td></tr>')))
                update_env(e, 'd', 1, False)
            e.set('offset', binary('+', e['offset'], 28))
        e.set('output', binary('+', e['output'], binary('+', binary('+', '<tr><td colspan="3" class="count">Found ', e['count']), ' matching item(s)</td></tr></tbody></table>\n')))
    else:
        if truth(binary('===', unary('typeof', e['offset']), 'undefined')):
            e.set('offset', binary('*', 28, call(get(e['Math'], 'floor'), binary('/', get(e['save'], 'daysPlayed'), 28))))
        if truth(binary('<', e['offset'], 112)):
            call(get(call(e['$'], '#book-prev-year'), 'prop'), 'disabled', True)
        else:
            call(get(call(e['$'], '#book-prev-year'), 'val'), binary('-', e['offset'], 112))
            call(get(call(e['$'], '#book-prev-year'), 'prop'), 'disabled', False)
        if truth(binary('<', e['offset'], 28)):
            call(get(call(e['$'], '#book-prev-month'), 'prop'), 'disabled', True)
        else:
            call(get(call(e['$'], '#book-prev-month'), 'val'), binary('-', e['offset'], 28))
            call(get(call(e['$'], '#book-prev-month'), 'prop'), 'disabled', False)
        call(get(call(e['$'], '#book-reset'), 'val'), 'reset')
        call(get(call(e['$'], '#book-reset'), 'html'), 'Reset Browsing')
        call(get(call(e['$'], '#book-next-month'), 'val'), binary('+', e['offset'], 28))
        call(get(call(e['$'], '#book-next-year'), 'val'), binary('+', e['offset'], 112))
        call(get(call(e['$'], '#book-search-text'), 'val'), '')
        call(get(call(e['$'], '#book-search-range'), 'val'), 2)
        call(get(call(e['$'], '#book-search-all'), 'prop'), 'checked', False)
        e.set('month', call(get(e['Math'], 'floor'), binary('/', e['offset'], 28)))
        e.set('seasonIndex', binary('%', e['month'], 4))
        e.set('monthName', get(get(e['save'], 'seasonNames'), e['seasonIndex']))
        e.set('year', binary('+', 1, call(get(e['Math'], 'floor'), binary('/', e['offset'], 112))))
        e.set('rng', call(e['CSRandom'], call(e['getRandomSeed'], binary('*', e['year'], 11), get(e['save'], 'gameID'), e['seasonIndex'])))
        e.set('possibleDays', Array([]))
        _switch270 = e['seasonIndex']
        _switch270_index = -1
        if _switch270_index < 0 and strict_equal(_switch270, 0): _switch270_index = 0
        if _switch270_index < 0 and strict_equal(_switch270, 1): _switch270_index = 1
        if _switch270_index < 0 and strict_equal(_switch270, 2): _switch270_index = 2
        if _switch270_index < 0 and strict_equal(_switch270, 3): _switch270_index = 3
        if _switch270_index < 0: _switch270_index = -1
        while True:
            if 0 <= _switch270_index <= 0:
                e.set('possibleDays', Array([11, 12, 21, 22, 25]))
                break
            if 0 <= _switch270_index <= 1:
                e.set('possibleDays', Array([9, 12, 18, 25, 27]))
                break
            if 0 <= _switch270_index <= 2:
                e.set('possibleDays', Array([4, 7, 8, 9, 12, 19, 22, 25]))
                break
            if 0 <= _switch270_index <= 3:
                e.set('possibleDays', Array([5, 11, 12, 19, 22, 24]))
                break
            break
        e.set('i', call(get(e['rng'], 'Next'), get(e['possibleDays'], 'length')))
        e.set('days', Array([get(e['possibleDays'], e['i']), get(e['possibleDays'], call(get(e['Math'], 'floor'), binary('%', binary('+', e['i'], binary('/', get(e['possibleDays'], 'length'), 2)), get(e['possibleDays'], 'length'))))]))
        call(get(e['days'], 'sort'), Fn(callback_271, e))
        e.set('output', binary('+', e['output'], '<table class="output"><thead><tr><th rowspan="2">Bookseller<br/>Items</th>'))
        e.set('d', 0)
        while truth(binary('<', e['d'], get(e['days'], 'length'))):
            e.set('output', binary('+', e['output'], binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', '<th colspan="2" class="multi">', get(get(e['save'], 'dayNames'), binary('%', binary('+', 6, get(e['days'], e['d'])), 7))), ' '), e['monthName']), ' '), get(e['days'], e['d'])), ', Year '), e['year']), '</th>')))
            update_env(e, 'd', 1, False)
        e.set('output', binary('+', e['output'], '</tr><tr>'))
        e.set('d', 0)
        while truth(binary('<', e['d'], get(e['days'], 'length'))):
            e.set('output', binary('+', e['output'], '<th class="item">Item</th><th class="price">Price</th>'))
            update_env(e, 'd', 1, False)
        e.set('output', binary('+', e['output'], '</tr></thead><tbody>'))
        e.set('tclass', 'current')
        e.set('monthsPlayed', call(get(e['Math'], 'floor'), binary('/', get(e['save'], 'daysPlayed'), 28)))
        if truth(binary('<', e['month'], e['monthsPlayed'])):
            e.set('tclass', 'past')
        else:
            if truth(binary('>', e['month'], e['monthsPlayed'])):
                e.set('tclass', 'future')
        e.set('stock', Obj({}))
        e.set('d', 0)
        while truth(binary('<', e['d'], get(e['days'], 'length'))):
            e.set('daysPlayed', binary('+', binary('+', e['offset'], get(e['days'], e['d'])), get(e['save'], 'dayAdjust')))
            put(e['stock'], e['d'], Obj({}))
            e.set('rng', call(e['CSRandom'], call(e['getRandomSeed'], e['daysPlayed'], binary('/', get(e['save'], 'gameID'), 2))))
            e.set('rngSynced', call(e['CSRandom'], call(e['getRandomSeed'], call(e['getHashFromString'], 'purplebookSale'), get(e['save'], 'gameID'), e['daysPlayed'])))
            if truth(binary('<', call(get(e['rngSynced'], 'NextDouble')), 0.25)):
                put(get(e['stock'], e['d']), 'purplebook', binary('+', binary('+', '<td class="book">', call(e['wikify'], 'Book Of Stars')), '</td><td>15,000g</td>'))
            else:
                put(get(e['stock'], e['d']), 'purplebook', '<td>--</td><td>--</td>')
            e.set('booksLeft', call(get(e['skillBookList'], 'slice')))
            e.set('rngSynced', call(e['CSRandom'], call(e['getRandomSeed'], call(e['getHashFromString'], 'thirdBookSale'), get(e['save'], 'gameID'), e['daysPlayed'])))
            if truth(binary('<', call(get(e['rngSynced'], 'NextDouble')), 0.6)):
                e.set('picked', call(get(e['booksLeft'], 'splice'), call(get(e['rng'], 'Next'), get(e['booksLeft'], 'length')), 1))
                put(get(e['stock'], e['d']), 'skill60pct', binary('+', binary('+', '<td class="book">', call(e['wikify'], get(e['picked'], 0))), '</td><td>10,000g</td>'))
            else:
                put(get(e['stock'], e['d']), 'skill60pct', '<td>--</td><td>--</td>')
            e.set('rngSynced', call(e['CSRandom'], call(e['getRandomSeed'], call(e['getHashFromString'], 'secondBookSale'), get(e['save'], 'gameID'), e['daysPlayed'])))
            if truth(binary('<', call(get(e['rngSynced'], 'NextDouble')), 0.8)):
                e.set('picked', call(get(e['booksLeft'], 'splice'), call(get(e['rng'], 'Next'), get(e['booksLeft'], 'length')), 1))
                put(get(e['stock'], e['d']), 'skill80pct', binary('+', binary('+', '<td class="book">', call(e['wikify'], get(e['picked'], 0))), '</td><td>8,000g</td>'))
            else:
                put(get(e['stock'], e['d']), 'skill80pct', '<td>--</td><td>--</td>')
            e.set('picked', call(get(e['booksLeft'], 'splice'), call(get(e['rng'], 'Next'), get(e['booksLeft'], 'length')), 1))
            put(get(e['stock'], e['d']), 'skillAlways', binary('+', binary('+', '<td class="book">', call(e['wikify'], get(e['picked'], 0))), '</td><td>5,000g</td>'))
            if truth(binary('>=', e['year'], 3)):
                e.set('picked', get(e['randBookList'], call(get(e['rng'], 'Next'), get(e['randBookList'], 'length'))))
                put(get(e['stock'], e['d']), 'y3', binary('+', binary('+', '<td class="book">', call(e['wikify'], e['picked'])), '</td><td>20,000g</td>'))
            else:
                put(get(e['stock'], e['d']), 'y3', '<td>--</td><td>--</td>')
            e.set('rngSynced', call(e['CSRandom'], call(e['getRandomSeed'], call(e['getHashFromString'], 'bookExtraForaging'), get(e['save'], 'gameID'), e['daysPlayed'])))
            if truth(binary('<', call(get(e['rngSynced'], 'NextDouble')), 0.33)):
                put(get(e['stock'], e['d']), 'foragebook', binary('+', binary('+', '<td class="book">', call(e['wikify'], "Woodcutter's Weekly")), '</td><td>8,000g</td>'))
            else:
                put(get(e['stock'], e['d']), 'foragebook', '<td>--</td><td>--</td>')
            update_env(e, 'd', 1, False)
        e.set('output', binary('+', e['output'], binary('+', binary('+', '<tr class="', e['tclass']), '"><td>Purple Book</td>')))
        e.set('d', 0)
        while truth(binary('<', e['d'], get(e['days'], 'length'))):
            e.set('output', binary('+', e['output'], get(get(e['stock'], e['d']), 'purplebook')))
            update_env(e, 'd', 1, False)
        e.set('output', binary('+', e['output'], '</tr>'))
        e.set('output', binary('+', e['output'], binary('+', binary('+', '<tr class="', e['tclass']), '"><td>Skill Book 1</td>')))
        e.set('d', 0)
        while truth(binary('<', e['d'], get(e['days'], 'length'))):
            e.set('output', binary('+', e['output'], get(get(e['stock'], e['d']), 'skill60pct')))
            update_env(e, 'd', 1, False)
        e.set('output', binary('+', e['output'], '</tr>'))
        e.set('output', binary('+', e['output'], binary('+', binary('+', '<tr class="', e['tclass']), '"><td>Skill Book 2</td>')))
        e.set('d', 0)
        while truth(binary('<', e['d'], get(e['days'], 'length'))):
            e.set('output', binary('+', e['output'], get(get(e['stock'], e['d']), 'skill80pct')))
            update_env(e, 'd', 1, False)
        e.set('output', binary('+', e['output'], '</tr>'))
        e.set('output', binary('+', e['output'], binary('+', binary('+', '<tr class="', e['tclass']), '"><td>Skill Book 3</td>')))
        e.set('d', 0)
        while truth(binary('<', e['d'], get(e['days'], 'length'))):
            e.set('output', binary('+', e['output'], get(get(e['stock'], e['d']), 'skillAlways')))
            update_env(e, 'd', 1, False)
        e.set('output', binary('+', e['output'], '</tr>'))
        e.set('output', binary('+', e['output'], binary('+', binary('+', '<tr class="', e['tclass']), '"><td>Random Y3 Book</td>')))
        e.set('d', 0)
        while truth(binary('<', e['d'], get(e['days'], 'length'))):
            e.set('output', binary('+', e['output'], get(get(e['stock'], e['d']), 'y3')))
            update_env(e, 'd', 1, False)
        e.set('output', binary('+', e['output'], '</tr>'))
        e.set('output', binary('+', e['output'], binary('+', binary('+', '<tr class="', e['tclass']), '"><td>Extra Book</td>')))
        e.set('d', 0)
        while truth(binary('<', e['d'], get(e['days'], 'length'))):
            e.set('output', binary('+', e['output'], get(get(e['stock'], e['d']), 'foragebook')))
            update_env(e, 'd', 1, False)
        e.set('output', binary('+', e['output'], '</tr>'))
        e.set('output', binary('+', e['output'], '</tbody></table>'))
    return e['output']
    return U


def predictStatues_272(parent, this, args):
    # Upstream predictor: 8535
    e = Env(parent)
    e.declare(['blessNoRain', 'blessRain', 'blessingNames', 'coords', 'day', 'dwarf1', 'dwarf1Text', 'dwarf2', 'dwarf2Text', 'dwarfNames', 'i', 'index', 'j', 'mapDim', 'month', 'monthName', 'noRainText', 'output', 'pbExtra', 'pbMaps', 'player', 'rainText', 'rng', 'roll', 'shard', 'tclass', 'week', 'weekDay', 'year'])
    e.local['arguments'] = Array(args)
    e.local['isSearch'] = (args[0] if len(args) > 0 and args[0] is not U else U)
    e.local['offset'] = (args[1] if len(args) > 1 and args[1] is not U else U)
    e.set('output', '')
    e.set('blessingNames', Array(['Speed', 'Luck', 'Energy', 'Waters', 'Friendship', 'Fangs', 'Butterfly']))
    e.set('dwarfNames', Array(['+1 Ore', 'Ladders', 'Coal', 'Bomb Immunity', 'Geodes']))
    e.set('pbMaps', Array(['Forest', 'Town', 'Beach', 'Mountain', 'Secret Woods', 'Bus Stop', 'Backwoods']))
    e.set('mapDim', Array([Array([120, 120]), Array([130, 110]), Array([104, 50]), Array([135, 41]), Array([60, 32]), Array([65, 30]), Array([50, 40])]))
    if truth(binary('===', unary('typeof', e['offset']), 'undefined')):
        e.set('offset', binary('*', 28, call(get(e['Math'], 'floor'), binary('/', get(e['save'], 'daysPlayed'), 28))))
    if truth(binary('<', e['offset'], 112)):
        call(get(call(e['$'], '#statue-prev-year'), 'prop'), 'disabled', True)
    else:
        call(get(call(e['$'], '#statue-prev-year'), 'val'), binary('-', e['offset'], 112))
        call(get(call(e['$'], '#statue-prev-year'), 'prop'), 'disabled', False)
    if truth(binary('<', e['offset'], 28)):
        call(get(call(e['$'], '#statue-prev-month'), 'prop'), 'disabled', True)
    else:
        call(get(call(e['$'], '#statue-prev-month'), 'val'), binary('-', e['offset'], 28))
        call(get(call(e['$'], '#statue-prev-month'), 'prop'), 'disabled', False)
    call(get(call(e['$'], '#statue-reset'), 'val'), 'reset')
    call(get(call(e['$'], '#statue-next-month'), 'val'), binary('+', e['offset'], 28))
    call(get(call(e['$'], '#statue-next-year'), 'val'), binary('+', e['offset'], 112))
    e.set('month', call(get(e['Math'], 'floor'), binary('/', e['offset'], 28)))
    e.set('monthName', get(get(e['save'], 'seasonNames'), binary('%', e['month'], 4)))
    e.set('year', binary('+', 1, call(get(e['Math'], 'floor'), binary('/', e['offset'], 112))))
    e.set('output', binary('+', e['output'], binary('+', binary('+', binary('+', binary('+', '<table class="calendar"><thead><tr><th colspan="7">', e['monthName']), ' Year '), e['year']), '</th></tr>\n')))
    e.set('output', binary('+', e['output'], '<tr><th>M</th><th>T</th><th>W</th><th>Th</th><th>F</th><th>Sa</th><th>Su</th></tr></thead>\n<tbody>'))
    e.set('week', 0)
    while truth(binary('<', e['week'], 4)):
        e.set('output', binary('+', e['output'], '<tr>'))
        e.set('weekDay', 1)
        while truth(binary('<', e['weekDay'], 8)):
            e.set('day', binary('+', binary('+', binary('*', 7, e['week']), e['weekDay']), e['offset']))
            e.set('rng', call(e['CSRandom'], call(e['getRandomSeed'], e['day'], binary('/', get(e['save'], 'gameID'), 2), binary('*', e['day'], 777))))
            e.set('j', 0)
            while truth(binary('<', e['j'], 8)):
                call(get(e['rng'], 'Next'))
                update_env(e, 'j', 1, False)
            e.set('roll', call(get(e['rng'], 'NextDouble')))
            e.set('blessRain', call(get(e['Math'], 'floor'), binary('*', e['roll'], 6)))
            e.set('blessNoRain', call(get(e['Math'], 'floor'), binary('*', e['roll'], 7)))
            e.set('pbExtra', '')
            if truth(binary('===', e['blessNoRain'], 6)):
                e.set('pbExtra', ' <span data-tooltip="Butterfly Spawns:\n')
                if truth(call(get(e['save'], 'hasOwnProperty'), 'mp_ids')):
                    e.set('player', 0)
                    while truth(binary('<', e['player'], get(get(e['save'], 'mp_ids'), 'length'))):
                        e.set('rng', call(e['CSRandom'], call(e['getRandomSeedFromBigInts'], call(e['bigInt'], e['day']), call(get(call(e['bigInt'], get(e['save'], 'gameID')), 'divide'), 2), call(get(get(get(e['save'], 'mp_ids'), e['player']), 'mod'), 10000))))
                        e.set('shard', binary('<', call(get(e['rng'], 'NextDouble')), binary('+', 0.05, get(e['save'], 'dailyLuck'))))
                        e.set('rng', call(e['CSRandom'], call(e['getRandomSeedFromBigInts'], call(e['bigInt'], e['day']), call(get(call(e['bigInt'], get(e['save'], 'gameID')), 'divide'), 2), call(get(get(get(e['save'], 'mp_ids'), e['player']), 'mod'), 10000))))
                        e.set('index', call(get(e['rng'], 'Next'), get(e['pbMaps'], 'length')))
                        e.set('pbExtra', binary('+', e['pbExtra'], binary('+', binary('+', binary('+', binary('+', binary('+', '&bull; ', get(get(e['save'], 'names'), e['player'])), ' - '), get(e['pbMaps'], e['index'])), (' (prismatic shard expected)' if truth(e['shard']) else '')), '\n')))
                        call(get(e['console'], 'log'), binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', 'Butterfly coordinate possibilities for ', get(get(e['save'], 'names'), e['player'])), ' - '), get(e['pbMaps'], e['index'])), ' on '), e['monthName']), ' '), binary('-', e['day'], e['offset'])), ', Y'), e['year']))
                        e.set('coords', Array([]))
                        e.set('i', 0)
                        while truth(binary('<=', e['i'], 32)):
                            call(get(e['coords'], 'push'), Obj({'x': call(get(e['rng'], 'Next'), get(get(e['mapDim'], e['index']), 0)), 'y': call(get(e['rng'], 'Next'), get(get(e['mapDim'], e['index']), 1))}))
                            update_env(e, 'i', 1, False)
                        call(get(e['console'], 'log'), e['coords'])
                        update_env(e, 'player', 1, False)
                else:
                    e.set('pbExtra', binary('+', e['pbExtra'], '(No players found)'))
                e.set('pbExtra', binary('+', e['pbExtra'], '">...</span>'))
            e.set('rng', call(e['CSRandom'], call(e['getRandomSeed'], binary('*', e['day'], 77), get(e['save'], 'gameID'))))
            e.set('dwarf1', call(get(e['rng'], 'Next'), 5))
            e.set('dwarf2', e['dwarf1'])
            while truth(binary('==', e['dwarf2'], e['dwarf1'])):
                e.set('dwarf2', call(get(e['rng'], 'Next'), 5))
            e.set('tclass', 'future')
            if truth(binary('<', e['day'], get(e['save'], 'daysPlayed'))):
                e.set('tclass', 'past')
            else:
                if truth(binary('===', e['day'], get(e['save'], 'daysPlayed'))):
                    e.set('tclass', 'current')
            e.set('rainText', get(e['blessingNames'], e['blessRain']))
            e.set('noRainText', binary('+', get(e['blessingNames'], e['blessNoRain']), e['pbExtra']))
            e.set('dwarf1Text', get(e['dwarfNames'], e['dwarf1']))
            e.set('dwarf2Text', get(e['dwarfNames'], e['dwarf2']))
            e.set('output', binary('+', e['output'], binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', '<td class="', e['tclass']), '"><span class="date"> '), binary('-', e['day'], e['offset'])), '</span><br/>'), '<span class="cell"><img src="blank.png" class="icon" alt="Umbrella in rain" id="bless_r"> '), e['rainText']), '<br/><img src="blank.png" class="icon" alt="Shining Sun" id="bless_nr"> '), e['noRainText']), '<hr /><img src="blank.png" class="icon" alt="Dwarf 1" id="bless_d1"> '), e['dwarf1Text']), '<br/><img src="blank.png" class="icon" alt="Dwarf 2" id="bless_d2"> '), e['dwarf2Text']), '</span></td>')))
            update_env(e, 'weekDay', 1, False)
        e.set('output', binary('+', e['output'], '</tr>\n'))
        update_env(e, 'week', 1, False)
    e.set('output', binary('+', e['output'], '<tr><td colspan="7" class="legend">Statue of Blessings: <img src="blank.png" class="icon" alt="Umbrella in rain" id="bless_r"> Blessing When Raining | <img src="blank.png" class="icon" alt="Shining Sun" id="bless_nr"> Blessing When Not Raining<br/>Statue of the Dwarf King: <img src="blank.png" class="icon" alt="Dwarf 1" id="bless_d1"> Choice 1 | <img src="blank.png" class="icon" alt="Dwarf 2" id="bless_d2"> Choice 2</td></tr>'))
    e.set('output', binary('+', e['output'], '</tbody></table>\n'))
    return e['output']
    return U


def predictPrizeTicket_273(parent, this, args):
    # Upstream predictor: 8632
    e = Env(parent)
    e.declare(['choice', 'count', 'g', 'item', 'itemQty', 'noLink', 'numOpened', 'o', 'output', 'pageSize', 'player', 'prefix', 'prizeLevel', 'randRoll', 'rng', 'rng2', 'searchEnd', 'searchResults', 'searchStart', 'searchTerm', 'tclass', 'whichPlayer'])
    e.local['arguments'] = Array(args)
    e.local['isSearch'] = (args[0] if len(args) > 0 and args[0] is not U else U)
    e.local['offset'] = (args[1] if len(args) > 1 and args[1] is not U else U)
    e.set('output', '')
    e.set('pageSize', 20)
    if truth((binary('!==', e['offset'], '') if truth(_logic274 := (binary('!==', unary('typeof', e['offset']), 'undefined') if truth(_logic275 := e['isSearch']) else _logic275)) else _logic274)):
        call(get(call(e['$'], '#prize-prev-100'), 'prop'), 'disabled', True)
        call(get(call(e['$'], '#prize-prev'), 'prop'), 'disabled', True)
        call(get(call(e['$'], '#prize-next'), 'prop'), 'disabled', True)
        call(get(call(e['$'], '#prize-next-100'), 'prop'), 'disabled', True)
        call(get(call(e['$'], '#prize-reset'), 'html'), 'Clear Search Results &amp; Reset Browsing')
        e.set('searchTerm', call(e['RegExp'], e['offset'], 'i'))
        e.set('searchStart', call(get(e['Math'], 'max'), 1, (1 if truth(call(get(call(e['$'], '#prize-search-all'), 'prop'), 'checked')) else get(get(e['save'], 'mysteryBoxesOpened'), 0))))
        e.set('searchEnd', binary('+', call(e['parseInt'], call(get(call(e['$'], '#prize-search-range'), 'val'))), e['searchStart']))
        e.set('output', binary('+', e['output'], binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', '<table class="output"><thead><tr><th colspan="', binary('+', e['numColumns'], 2)), '">Search results for &quot;'), e['offset']), '&quot; over the '), ('first ' if truth(call(get(call(e['$'], '#prize-search-all'), 'prop'), 'checked')) else 'next ')), call(get(call(e['$'], '#prize-search-range'), 'val'))), ' prize claims</th></tr>\n')))
        e.set('output', binary('+', e['output'], '<tr><th class="item">Item</th><th class="mystery-result">Prize Received</th></tr><tbody>'))
        e.set('count', 0)
        e.set('searchResults', Obj({}))
        e.set('output', binary('+', e['output'], '</table>'))
    else:
        e.set('whichPlayer', 0)
        if truth((binary('>', get(get(e['save'], 'mp_ids'), 'length'), 1) if truth(_logic276 := binary('!==', unary('typeof', get(e['save'], 'mp_ids')), 'undefined')) else _logic276)):
            call(get(call(e['$'], '#prize-player'), 'show'))
            if truth(binary('==', get(call(e['$'], '#prize-player-select option'), 'length'), 0)):
                e.set('player', 0)
                while truth(binary('<', e['player'], get(get(e['save'], 'mp_ids'), 'length'))):
                    e.set('prefix', ('Main Farmer ' if truth(binary('==', e['player'], 0)) else 'Farmhand '))
                    e.set('o', call(e['Option'], binary('+', e['prefix'], get(get(e['save'], 'names'), e['player'])), e['player']))
                    if truth(binary('==', e['player'], 0)):
                        put(e['o'], 'selected', True)
                    call(get(call(e['$'], '#prize-player-select'), 'append'), e['o'])
                    update_env(e, 'player', 1, False)
            else:
                e.set('whichPlayer', call(get(call(e['$'], '#prize-player-select'), 'val')))
        else:
            call(get(call(e['$'], '#prize-player'), 'hide'))
        if truth(binary('===', unary('typeof', e['offset']), 'undefined')):
            e.set('offset', binary('*', e['pageSize'], call(get(e['Math'], 'floor'), binary('/', get(get(e['save'], 'ticketPrizesClaimed'), e['whichPlayer']), e['pageSize']))))
        if truth(binary('<', e['offset'], e['pageSize'])):
            call(get(call(e['$'], '#prize-prev'), 'prop'), 'disabled', True)
        else:
            call(get(call(e['$'], '#prize-prev'), 'val'), binary('-', e['offset'], e['pageSize']))
            call(get(call(e['$'], '#prize-prev'), 'prop'), 'disabled', False)
        if truth(binary('<', e['offset'], 100)):
            call(get(call(e['$'], '#prize-prev-100'), 'prop'), 'disabled', True)
        else:
            call(get(call(e['$'], '#prize-prev-100'), 'val'), binary('-', e['offset'], 100))
            call(get(call(e['$'], '#prize-prev-100'), 'prop'), 'disabled', False)
        call(get(call(e['$'], '#prize-reset'), 'val'), 'reset')
        call(get(call(e['$'], '#prize-reset'), 'html'), 'Reset Browsing')
        call(get(call(e['$'], '#prize-next'), 'val'), binary('+', e['offset'], e['pageSize']))
        call(get(call(e['$'], '#prize-next'), 'prop'), 'disabled', False)
        call(get(call(e['$'], '#prize-next-100'), 'val'), binary('+', e['offset'], 100))
        call(get(call(e['$'], '#prize-next-100'), 'prop'), 'disabled', False)
        call(get(call(e['$'], '#prize-search-text'), 'val'), '')
        call(get(call(e['$'], '#prize-search-range'), 'val'), 200)
        call(get(call(e['$'], '#prize-search-all'), 'prop'), 'checked', False)
        e.set('output', binary('+', e['output'], binary('+', '<table class="output"><thead><tr><th rowspan="2" class="index">Num Open</th>', '<th colspan="2" class="prize-result">Prize Received</th>')))
        e.set('output', binary('+', e['output'], '</tr><tr><th class="item">Item</th><th class="qty">Qty</th></tr><tbody>'))
        if truth(binary('!==', unary('typeof', get(e['save'], 'mp_ids')), 'undefined')):
            e.set('rng', call(e['CSRandom'], call(e['getRandomSeedFromBigInts'], call(e['bigInt'], get(e['save'], 'gameID')), get(get(e['save'], 'mp_ids'), e['whichPlayer']))))
        else:
            e.set('rng', call(e['CSRandom'], call(e['getRandomSeed'], get(e['save'], 'gameID'), 0)))
            call(get(call(e['$'], '#prize-note'), 'html'), 'Note: No players found; predictions will not be reliable')
        e.set('randRoll', call(get(e['rng'], 'NextDouble')))
        e.set('g', 1)
        while truth(binary('<=', e['g'], e['pageSize'])):
            e.set('numOpened', binary('+', e['offset'], e['g']))
            e.set('prizeLevel', binary('-', e['numOpened'], 1))
            e.set('item', '')
            e.set('itemQty', 1)
            e.set('noLink', False)
            _switch277 = e['prizeLevel']
            _switch277_index = -1
            if _switch277_index < 0 and strict_equal(_switch277, 0): _switch277_index = 0
            if _switch277_index < 0 and strict_equal(_switch277, 1): _switch277_index = 1
            if _switch277_index < 0 and strict_equal(_switch277, 2): _switch277_index = 2
            if _switch277_index < 0 and strict_equal(_switch277, 3): _switch277_index = 3
            if _switch277_index < 0 and strict_equal(_switch277, 15): _switch277_index = 4
            if _switch277_index < 0 and strict_equal(_switch277, 4): _switch277_index = 5
            if _switch277_index < 0 and strict_equal(_switch277, 5): _switch277_index = 6
            if _switch277_index < 0 and strict_equal(_switch277, 6): _switch277_index = 7
            if _switch277_index < 0 and strict_equal(_switch277, 7): _switch277_index = 8
            if _switch277_index < 0 and strict_equal(_switch277, 8): _switch277_index = 9
            if _switch277_index < 0 and strict_equal(_switch277, 9): _switch277_index = 10
            if _switch277_index < 0 and strict_equal(_switch277, 10): _switch277_index = 11
            if _switch277_index < 0 and strict_equal(_switch277, 11): _switch277_index = 12
            if _switch277_index < 0 and strict_equal(_switch277, 12): _switch277_index = 13
            if _switch277_index < 0 and strict_equal(_switch277, 13): _switch277_index = 14
            if _switch277_index < 0 and strict_equal(_switch277, 14): _switch277_index = 15
            if _switch277_index < 0 and strict_equal(_switch277, 16): _switch277_index = 16
            if _switch277_index < 0 and strict_equal(_switch277, 17): _switch277_index = 17
            if _switch277_index < 0 and strict_equal(_switch277, 18): _switch277_index = 18
            if _switch277_index < 0 and strict_equal(_switch277, 19): _switch277_index = 19
            if _switch277_index < 0 and strict_equal(_switch277, 20): _switch277_index = 20
            if _switch277_index < 0 and strict_equal(_switch277, 21): _switch277_index = 21
            if _switch277_index < 0: _switch277_index = 22
            while True:
                if 0 <= _switch277_index <= 0:
                    e.set('item', 'Raccoon Seeds')
                    e.set('itemQty', 12)
                    e.set('noLink', True)
                    break
                if 0 <= _switch277_index <= 1:
                    e.set('item', ('Peach Sapling' if truth(binary('<', e['randRoll'], 0.5)) else 'Orange Sapling'))
                    break
                if 0 <= _switch277_index <= 2:
                    if truth(binary('<', e['randRoll'], 0.5)):
                        e.set('item', 'Mixed Seeds')
                        e.set('itemQty', 10)
                    else:
                        e.set('item', 'Mixed Flower Seeds')
                        e.set('itemQty', 15)
                    break
                if 0 <= _switch277_index <= 3:
                    e.set('item', 'Mystery Box')
                    e.set('itemQty', 3)
                    break
                if 0 <= _switch277_index <= 4:
                    pass
                if 0 <= _switch277_index <= 5:
                    e.set('item', 'Stardrop Tea')
                    break
                if 0 <= _switch277_index <= 6:
                    e.set('item', call(e['wikify'], 'Blue Pinstripe Bed', 'Furniture'))
                    e.set('noLink', True)
                    break
                if 0 <= _switch277_index <= 7:
                    _switch278 = call(get(e['Math'], 'floor'), binary('*', 3, e['randRoll']))
                    _switch278_index = -1
                    if _switch278_index < 0 and strict_equal(_switch278, 0): _switch278_index = 0
                    if _switch278_index < 0 and strict_equal(_switch278, 1): _switch278_index = 1
                    if _switch278_index < 0 and strict_equal(_switch278, 2): _switch278_index = 2
                    if _switch278_index < 0: _switch278_index = -1
                    while True:
                        if 0 <= _switch278_index <= 0:
                            e.set('item', 'Quality Sprinkler')
                            break
                        if 0 <= _switch278_index <= 1:
                            e.set('item', 'Preserves Jar')
                            break
                        if 0 <= _switch278_index <= 2:
                            e.set('item', 'Mushroom Log')
                            break
                        break
                    e.set('itemQty', 4)
                    break
                if 0 <= _switch277_index <= 8:
                    e.set('item', ('Apple Sapling' if truth(binary('<', e['randRoll'], 0.5)) else 'Pomegranate Sapling'))
                    break
                if 0 <= _switch277_index <= 9:
                    e.set('item', binary('+', binary('+', '<span class="book">', call(e['wikify'], 'Friendship 101')), '</span>'))
                    e.set('noLink', True)
                    break
                if 0 <= _switch277_index <= 10:
                    _switch279 = call(get(e['Math'], 'floor'), binary('*', 3, e['randRoll']))
                    _switch279_index = -1
                    if _switch279_index < 0 and strict_equal(_switch279, 0): _switch279_index = 0
                    if _switch279_index < 0 and strict_equal(_switch279, 1): _switch279_index = 1
                    if _switch279_index < 0 and strict_equal(_switch279, 2): _switch279_index = 2
                    if _switch279_index < 0: _switch279_index = -1
                    while True:
                        if 0 <= _switch279_index <= 0:
                            e.set('item', 'Cherry Bomb')
                            e.set('itemQty', 20)
                            break
                        if 0 <= _switch279_index <= 1:
                            e.set('item', 'Bomb')
                            e.set('itemQty', 12)
                            break
                        if 0 <= _switch279_index <= 2:
                            e.set('item', 'Mega Bomb')
                            e.set('itemQty', 6)
                            break
                        break
                    break
                if 0 <= _switch277_index <= 11:
                    e.set('item', call(e['wikify'], 'Sports Cap', 'Hats'))
                    e.set('noLink', True)
                    break
                if 0 <= _switch277_index <= 12:
                    e.set('item', ('Fish Smoker' if truth(binary('<', e['randRoll'], 0.5)) else 'Dehydrator'))
                    break
                if 0 <= _switch277_index <= 13:
                    e.set('item', ('Artifact Trove' if truth(binary('<', e['randRoll'], 0.5)) else 'Mystery Box'))
                    e.set('itemQty', 4)
                    break
                if 0 <= _switch277_index <= 14:
                    e.set('choice', Array(['House Plant (1)', 'House Plant (2)', 'House Plant (3)']))
                    e.set('item', call(e['wikify'], get(e['choice'], call(get(e['Math'], 'floor'), binary('*', e['randRoll'], get(e['choice'], 'length')))), 'Furniture'))
                    e.set('noLink', True)
                    break
                if 0 <= _switch277_index <= 15:
                    e.set('choice', Array(['Stardew Valley Almanac', 'Bait And Bobber', "Woodcutter's Weekly", 'Mining Monthly', 'Combat Quarterly']))
                    e.set('item', binary('+', binary('+', '<span class="book">', call(e['wikify'], get(e['choice'], call(get(e['Math'], 'floor'), binary('*', e['randRoll'], get(e['choice'], 'length')))))), '</span>'))
                    e.set('noLink', True)
                    break
                if 0 <= _switch277_index <= 16:
                    e.set('item', call(e['wikify'], 'Cow Decal', 'Furniture'))
                    e.set('noLink', True)
                    break
                if 0 <= _switch277_index <= 17:
                    e.set('item', 'Omni Geode')
                    e.set('itemQty', 8)
                    break
                if 0 <= _switch277_index <= 18:
                    e.set('item', ('Bee House' if truth(binary('<', e['randRoll'], 0.5)) else 'Keg'))
                    e.set('itemQty', 4)
                    break
                if 0 <= _switch277_index <= 19:
                    e.set('item', 'Diamond')
                    e.set('itemQty', 5)
                    break
                if 0 <= _switch277_index <= 20:
                    e.set('item', 'Mystery Box')
                    e.set('itemQty', 5)
                    break
                if 0 <= _switch277_index <= 21:
                    e.set('item', 'Magic Rock Candy')
                    break
                if 0 <= _switch277_index <= 22:
                    e.set('rng2', call(e['CSRandom'], call(e['getRandomSeed'], get(e['save'], 'gameID'), binary('-', e['prizeLevel'], binary('%', e['prizeLevel'], 9)))))
                    _switch280 = binary('%', e['prizeLevel'], 9)
                    _switch280_index = -1
                    if _switch280_index < 0 and strict_equal(_switch280, 0): _switch280_index = 0
                    if _switch280_index < 0 and strict_equal(_switch280, 1): _switch280_index = 1
                    if _switch280_index < 0 and strict_equal(_switch280, 2): _switch280_index = 2
                    if _switch280_index < 0 and strict_equal(_switch280, 3): _switch280_index = 3
                    if _switch280_index < 0 and strict_equal(_switch280, 4): _switch280_index = 4
                    if _switch280_index < 0 and strict_equal(_switch280, 5): _switch280_index = 5
                    if _switch280_index < 0 and strict_equal(_switch280, 6): _switch280_index = 6
                    if _switch280_index < 0 and strict_equal(_switch280, 7): _switch280_index = 7
                    if _switch280_index < 0 and strict_equal(_switch280, 8): _switch280_index = 8
                    if _switch280_index < 0: _switch280_index = 9
                    while True:
                        if 0 <= _switch280_index <= 0:
                            e.set('item', 'Mystery Box')
                            e.set('itemQty', 5)
                            break
                        if 0 <= _switch280_index <= 1:
                            e.set('item', 'Fairy Dust')
                            e.set('itemQty', call(get(e['rng2'], 'Next'), 1, 3))
                            break
                        if 0 <= _switch280_index <= 2:
                            e.set('choice', Array(['Iridium Bar', 'Spicy Eel', 'Triple Shot Espresso', 'Crab Cakes', 'Artifact Trove']))
                            e.set('item', get(e['choice'], call(get(e['rng2'], 'Next'), get(e['choice'], 'length'))))
                            e.set('itemQty', 5)
                            break
                        if 0 <= _switch280_index <= 3:
                            e.set('choice', Array(['House Plant (1)', 'House Plant (2)', 'House Plant (3)']))
                            e.set('item', call(e['wikify'], get(e['choice'], call(get(e['rng2'], 'Next'), get(e['choice'], 'length'))), 'Furniture'))
                            e.set('noLink', True)
                            break
                        if 0 <= _switch280_index <= 4:
                            e.set('item', 'Stardrop Tea')
                            break
                        if 0 <= _switch280_index <= 5:
                            e.set('item', 'Treasure Chest')
                            break
                        if 0 <= _switch280_index <= 6:
                            e.set('item', 'Iridium Sprinkler')
                            break
                        if 0 <= _switch280_index <= 7:
                            e.set('choice', Array(['Fancy House Plant (1)', 'Fancy House Plant (2)', 'Fancy House Plant (3)', 'Pig Painting']))
                            e.set('item', call(e['wikify'], get(e['choice'], call(get(e['rng2'], 'Next'), get(e['choice'], 'length'))), 'Furniture'))
                            e.set('noLink', True)
                            break
                        if 0 <= _switch280_index <= 8:
                            _switch281 = call(get(e['rng2'], 'Next'), 2)
                            _switch281_index = -1
                            if _switch281_index < 0 and strict_equal(_switch281, 0): _switch281_index = 0
                            if _switch281_index < 0 and strict_equal(_switch281, 1): _switch281_index = 1
                            if _switch281_index < 0: _switch281_index = -1
                            while True:
                                if 0 <= _switch281_index <= 0:
                                    e.set('item', 'Bomb')
                                    e.set('itemQty', 15)
                                    break
                                if 0 <= _switch281_index <= 1:
                                    e.set('item', 'Mega Bomb')
                                    e.set('itemQty', 8)
                                    break
                                break
                            break
                        if 0 <= _switch280_index <= 9:
                            e.set('item', 'Mystery Box')
                            e.set('itemQty', 5)
                        break
                break
            e.set('tclass', 'future')
            if truth(binary('===', e['numOpened'], binary('+', get(get(e['save'], 'ticketPrizesClaimed'), e['whichPlayer']), 1))):
                e.set('tclass', 'current')
            else:
                if truth(binary('<=', e['numOpened'], get(get(e['save'], 'ticketPrizesClaimed'), e['whichPlayer']))):
                    e.set('tclass', 'past')
            e.set('output', binary('+', e['output'], binary('+', binary('+', binary('+', binary('+', '<tr class="', e['tclass']), '"><td>'), call(e['addCommas'], e['numOpened'])), '</td>')))
            e.set('output', binary('+', e['output'], binary('+', binary('+', binary('+', binary('+', '<td class="item">', (e['item'] if truth(e['noLink']) else call(e['wikify'], e['item']))), '</td><td>'), e['itemQty']), '</td>')))
            e.set('output', binary('+', e['output'], '</tr>'))
            update_env(e, 'g', 1, False)
    e.set('output', binary('+', e['output'], '</tbody></table>'))
    return e['output']
    return U


def predictRaccoon_282(parent, this, args):
    # Upstream predictor: 8839
    e = Env(parent)
    e.declare(['bundleItem', 'bundleQty', 'choice', 'count', 'g', 'i', 'index', 'isLong', 'output', 'pageSize', 'piece', 'prevRoll', 'rng', 's', 'searchEnd', 'searchResults', 'searchStart', 'searchTerm', 'tableRow', 'tclass', 'timesFed', 'whichBundle'])
    e.local['arguments'] = Array(args)
    e.local['isSearch'] = (args[0] if len(args) > 0 and args[0] is not U else U)
    e.local['offset'] = (args[1] if len(args) > 1 and args[1] is not U else U)
    e.set('output', '')
    e.set('pageSize', 10)
    if truth((binary('!==', e['offset'], '') if truth(_logic283 := (binary('!==', unary('typeof', e['offset']), 'undefined') if truth(_logic284 := e['isSearch']) else _logic284)) else _logic283)):
        call(get(call(e['$'], '#raccoon-prev-50'), 'prop'), 'disabled', True)
        call(get(call(e['$'], '#raccoon-prev'), 'prop'), 'disabled', True)
        call(get(call(e['$'], '#raccoon-next'), 'prop'), 'disabled', True)
        call(get(call(e['$'], '#raccoon-next-50'), 'prop'), 'disabled', True)
        call(get(call(e['$'], '#raccoon-reset'), 'html'), 'Clear Search Results &amp; Reset Browsing')
        e.set('searchTerm', call(e['RegExp'], e['offset'], 'i'))
        e.set('searchStart', call(get(e['Math'], 'max'), 1, (1 if truth(call(get(call(e['$'], '#raccoon-search-all'), 'prop'), 'checked')) else get(get(e['save'], 'mysteryBoxesOpened'), 0))))
        e.set('searchEnd', binary('+', call(e['parseInt'], call(get(call(e['$'], '#raccoon-search-range'), 'val'))), e['searchStart']))
        e.set('output', binary('+', e['output'], binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', '<table class="output"><thead><tr><th colspan="', binary('+', e['numColumns'], 2)), '">Search results for &quot;'), e['offset']), '&quot; over the '), ('first ' if truth(call(get(call(e['$'], '#raccoon-search-all'), 'prop'), 'checked')) else 'next ')), call(get(call(e['$'], '#raccoon-search-range'), 'val'))), ' raccoon requests</th></tr>')))
        e.set('output', binary('+', e['output'], '<tbody>'))
        e.set('count', 0)
        e.set('searchResults', Obj({}))
        e.set('output', binary('+', e['output'], binary('+', binary('+', binary('+', binary('+', '<tr><td colspan="2" class="count">Found ', e['count']), ' matching instance(s) of '), get(call(get(e['Object'], 'keys'), e['searchResults']), 'length')), ' matching item(s)</td></tr></tbody></table>')))
    else:
        if truth(binary('===', unary('typeof', e['offset']), 'undefined')):
            e.set('offset', binary('*', e['pageSize'], call(get(e['Math'], 'floor'), binary('/', get(e['save'], 'timesFedRaccoons'), e['pageSize']))))
        if truth(binary('<', e['offset'], e['pageSize'])):
            call(get(call(e['$'], '#raccoon-prev'), 'prop'), 'disabled', True)
        else:
            call(get(call(e['$'], '#raccoon-prev'), 'val'), binary('-', e['offset'], e['pageSize']))
            call(get(call(e['$'], '#raccoon-prev'), 'prop'), 'disabled', False)
        if truth(binary('<', e['offset'], 50)):
            call(get(call(e['$'], '#raccoon-prev-50'), 'prop'), 'disabled', True)
        else:
            call(get(call(e['$'], '#raccoon-prev-50'), 'val'), binary('-', e['offset'], 50))
            call(get(call(e['$'], '#raccoon-prev-50'), 'prop'), 'disabled', False)
        call(get(call(e['$'], '#raccoon-reset'), 'val'), 'reset')
        call(get(call(e['$'], '#raccoon-reset'), 'html'), 'Reset Browsing')
        call(get(call(e['$'], '#raccoon-next'), 'val'), binary('+', e['offset'], e['pageSize']))
        call(get(call(e['$'], '#raccoon-next'), 'prop'), 'disabled', False)
        call(get(call(e['$'], '#raccoon-next-50'), 'val'), binary('+', e['offset'], 50))
        call(get(call(e['$'], '#raccoon-next-50'), 'prop'), 'disabled', False)
        call(get(call(e['$'], '#raccoon-search-text'), 'val'), '')
        call(get(call(e['$'], '#raccoon-search-range'), 'val'), 200)
        call(get(call(e['$'], '#raccoon-search-all'), 'prop'), 'checked', False)
        e.set('output', binary('+', e['output'], binary('+', binary('+', binary('+', '<table class="output"><thead><tr><th rowspan="2" class="index">Times Fed</th>', '<th colspan="2" class="raccoon-result">First Requested Item</th>'), '<th colspan="2" class="raccoon-result">Second Requested Item</th>'), '<th colspan="2" class="raccoon-result">Reward Received</th>')))
        e.set('output', binary('+', e['output'], '</tr><tr><th class="item">Item</th><th class="qty">Qty</th><th class="item">Item</th><th class="qty">Qty</th><th class="item">Item</th><th class="qty">Qty</th></tr><tbody>'))
        e.set('g', 1)
        while truth(binary('<=', e['g'], e['pageSize'])):
            e.set('tableRow', binary('+', e['offset'], e['g']))
            e.set('timesFed', binary('-', e['tableRow'], 1))
            e.set('prevRoll', Array([]))
            e.set('rng', Array([]))
            e.set('s', 0)
            while truth(binary('<', e['s'], 4)):
                put(e['rng'], e['s'], call(e['CSRandom'], call(e['getRandomSeed'], get(e['save'], 'gameID'), binary('*', e['timesFed'], 377))))
                e.set('i', 0)
                while truth(binary('<', e['i'], 10)):
                    call(get(get(e['rng'], e['s']), 'Next'))
                    update_env(e, 'i', 1, False)
                update_env(e, 's', 1, False)
            e.set('bundleItem', Array([]))
            e.set('bundleQty', Array([1, 1, 1]))
            e.set('isLong', Array([False, False, False]))
            if truth(binary('<', e['timesFed'], 5)):
                e.set('whichBundle', binary('%', e['timesFed'], 5))
            else:
                e.set('whichBundle', call(get(get(e['rng'], 0), 'Next'), 5))
                e.set('s', 1)
                while truth(binary('<', e['s'], 4)):
                    call(get(get(e['rng'], e['s']), 'Next'))
                    update_env(e, 's', 1, False)
            _switch285 = e['whichBundle']
            _switch285_index = -1
            if _switch285_index < 0 and strict_equal(_switch285, 0): _switch285_index = 0
            if _switch285_index < 0 and strict_equal(_switch285, 1): _switch285_index = 1
            if _switch285_index < 0 and strict_equal(_switch285, 2): _switch285_index = 2
            if _switch285_index < 0 and strict_equal(_switch285, 3): _switch285_index = 3
            if _switch285_index < 0 and strict_equal(_switch285, 4): _switch285_index = 4
            if _switch285_index < 0: _switch285_index = -1
            while True:
                if 0 <= _switch285_index <= 0:
                    e.set('choice', Array(['_722', '_721', '_716', '_719', '_723', '_718', '_372']))
                    put(e['bundleItem'], 0, call(e['wikify'], get(get(get(e['save'], 'objects'), get(e['choice'], call(get(get(e['rng'], 0), 'Next'), get(e['choice'], 'length')))), 'name')))
                    e.set('s', 1)
                    while truth(binary('<', e['s'], 4)):
                        call(get(get(e['rng'], e['s']), 'Next'))
                        update_env(e, 's', 1, False)
                    put(e['bundleQty'], 0, 5)
                    e.set('choice', table(23))
                    put(e['bundleItem'], 1, '')
                    put(e['bundleQty'], 1, 1)
                    put(e['isLong'], 1, True)
                    put(e['bundleItem'], 1, Array([]))
                    e.set('s', 0)
                    while truth(binary('<', e['s'], 4)):
                        e.set('index', call(get(get(e['rng'], e['s']), 'Next'), get(get(e['choice'], e['s']), 'length')))
                        put(get(e['bundleItem'], 1), e['s'], call(e['wikify'], binary('+', 'Smoked ', get(get(get(e['save'], 'objects'), get(get(e['choice'], e['s']), e['index'])), 'name'))))
                        update_env(e, 's', 1, False)
                    break
                if 0 <= _switch285_index <= 1:
                    e.set('choice', table(24))
                    put(e['isLong'], 0, True)
                    put(e['bundleItem'], 0, Array([]))
                    e.set('s', 0)
                    while truth(binary('<', e['s'], 4)):
                        e.set('index', call(get(get(e['rng'], e['s']), 'Next'), get(get(e['choice'], e['s']), 'length')))
                        put(get(e['bundleItem'], 0), e['s'], call(e['wikify'], binary('+', 'Dried ', get(get(get(e['save'], 'objects'), get(get(e['choice'], e['s']), e['index'])), 'name'))))
                        put(e['prevRoll'], e['s'], e['index'])
                        update_env(e, 's', 1, False)
                    put(e['isLong'], 1, True)
                    put(e['bundleItem'], 1, Array([]))
                    e.set('s', 0)
                    while truth(binary('<', e['s'], 4)):
                        e.set('index', get(e['prevRoll'], e['s']))
                        while truth(binary('===', e['index'], get(e['prevRoll'], e['s']))):
                            e.set('index', call(get(get(e['rng'], e['s']), 'Next'), get(get(e['choice'], e['s']), 'length')))
                        put(get(e['bundleItem'], 1), e['s'], call(e['wikify'], binary('+', get(get(get(e['save'], 'objects'), get(get(e['choice'], e['s']), e['index'])), 'name'), ' Jelly')))
                        update_env(e, 's', 1, False)
                    break
                if 0 <= _switch285_index <= 2:
                    e.set('choice', Array([Array(['_422', '_404', '_257']), Array(['_422', '_404']), Array(['_422', '_404', '_281']), Array(['_422', '_404'])]))
                    put(e['isLong'], 0, True)
                    put(e['bundleItem'], 0, Array([]))
                    e.set('s', 0)
                    while truth(binary('<', e['s'], 4)):
                        e.set('index', call(get(get(e['rng'], e['s']), 'Next'), get(get(e['choice'], e['s']), 'length')))
                        put(get(e['bundleItem'], 0), e['s'], call(e['wikify'], binary('+', 'Dried ', get(get(get(e['save'], 'objects'), get(get(e['choice'], e['s']), e['index'])), 'name'))))
                        put(e['prevRoll'], e['s'], e['index'])
                        update_env(e, 's', 1, False)
                    e.set('choice', Array(['Egg (Any)', 'Cave Carrot', 'White Algae']))
                    put(e['bundleItem'], 1, call(e['wikify'], get(e['choice'], call(get(get(e['rng'], 0), 'Next'), get(e['choice'], 'length')))))
                    put(e['bundleQty'], 1, 5)
                    break
                if 0 <= _switch285_index <= 3:
                    e.set('choice', table(25))
                    put(e['isLong'], 0, True)
                    put(e['bundleItem'], 0, Array([]))
                    e.set('s', 0)
                    while truth(binary('<', e['s'], 4)):
                        e.set('index', call(get(get(e['rng'], e['s']), 'Next'), get(get(e['choice'], e['s']), 'length')))
                        put(get(e['bundleItem'], 0), e['s'], call(e['wikify'], binary('+', get(get(get(e['save'], 'objects'), get(get(e['choice'], e['s']), e['index'])), 'name'), ' Juice')))
                        put(e['prevRoll'], e['s'], e['index'])
                        update_env(e, 's', 1, False)
                    put(e['isLong'], 1, True)
                    put(e['bundleItem'], 1, Array([]))
                    e.set('s', 0)
                    while truth(binary('<', e['s'], 4)):
                        e.set('index', get(e['prevRoll'], e['s']))
                        while truth(binary('===', e['index'], get(e['prevRoll'], e['s']))):
                            e.set('index', call(get(get(e['rng'], e['s']), 'Next'), get(get(e['choice'], e['s']), 'length')))
                        put(get(e['bundleItem'], 1), e['s'], call(e['wikify'], binary('+', 'Pickled ', get(get(get(e['save'], 'objects'), get(get(e['choice'], e['s']), e['index'])), 'name'))))
                        update_env(e, 's', 1, False)
                    break
                if 0 <= _switch285_index <= 4:
                    e.set('choice', Array(['Moss_10', '110_1', '168_5', '766_99', '767_20', '535_8', '536_5', '537_3', '393_4', '397_2', '684_20', '72_1', '68_3', '156_3']))
                    e.set('index', call(get(get(e['rng'], 0), 'Next'), get(e['choice'], 'length')))
                    e.set('piece', call(get(get(e['choice'], e['index']), 'split'), '_'))
                    put(e['bundleItem'], 0, call(e['wikify'], get(get(get(e['save'], 'objects'), binary('+', '_', get(e['piece'], 0))), 'name')))
                    put(e['bundleQty'], 0, get(e['piece'], 1))
                    put(e['prevRoll'], 0, e['index'])
                    while truth(binary('===', e['index'], get(e['prevRoll'], 0))):
                        e.set('index', call(get(get(e['rng'], 0), 'Next'), get(e['choice'], 'length')))
                    e.set('piece', call(get(get(e['choice'], e['index']), 'split'), '_'))
                    put(e['bundleItem'], 1, call(e['wikify'], get(get(get(e['save'], 'objects'), binary('+', '_', get(e['piece'], 0))), 'name')))
                    put(e['bundleQty'], 1, get(e['piece'], 1))
                    break
                break
            _switch286 = e['tableRow']
            _switch286_index = -1
            if _switch286_index < 0 and strict_equal(_switch286, 1): _switch286_index = 0
            if _switch286_index < 0 and strict_equal(_switch286, 2): _switch286_index = 1
            if _switch286_index < 0 and strict_equal(_switch286, 3): _switch286_index = 2
            if _switch286_index < 0 and strict_equal(_switch286, 4): _switch286_index = 3
            if _switch286_index < 0 and strict_equal(_switch286, 5): _switch286_index = 4
            if _switch286_index < 0: _switch286_index = 5
            while True:
                if 0 <= _switch286_index <= 0:
                    put(e['bundleItem'], 2, 'Raccoon Seeds')
                    put(e['bundleQty'], 2, 25)
                    break
                if 0 <= _switch286_index <= 1:
                    put(e['bundleItem'], 2, binary('+', binary('+', '<span class="book">', call(e['wikify'], 'Raccoon Journal')), '</span>'))
                    break
                if 0 <= _switch286_index <= 2:
                    put(e['bundleItem'], 2, call(e['wikify'], 'Raccoon Hat', 'Hats'))
                    break
                if 0 <= _switch286_index <= 3:
                    put(e['bundleItem'], 2, call(e['wikify'], 'Fairy Dust'))
                    put(e['bundleQty'], 2, 7)
                    break
                if 0 <= _switch286_index <= 4:
                    put(e['bundleItem'], 2, call(e['wikify'], 'Jungle Tank', 'Furniture'))
                    break
                if 0 <= _switch286_index <= 5:
                    e.set('rng', call(e['CSRandom'], call(e['getRandomSeed'], get(e['save'], 'gameID'), binary('*', e['tableRow'], 377))))
                    e.set('i', 0)
                    while truth(binary('<', e['i'], 10)):
                        call(get(e['rng'], 'Next'))
                        update_env(e, 'i', 1, False)
                    _switch287 = call(get(e['rng'], 'Next'), 5)
                    _switch287_index = -1
                    if _switch287_index < 0 and strict_equal(_switch287, 0): _switch287_index = 0
                    if _switch287_index < 0 and strict_equal(_switch287, 1): _switch287_index = 1
                    if _switch287_index < 0 and strict_equal(_switch287, 2): _switch287_index = 2
                    if _switch287_index < 0 and strict_equal(_switch287, 3): _switch287_index = 3
                    if _switch287_index < 0 and strict_equal(_switch287, 4): _switch287_index = 4
                    if _switch287_index < 0: _switch287_index = 5
                    while True:
                        if 0 <= _switch287_index <= 0:
                            put(e['bundleItem'], 2, call(e['wikify'], 'Fairy Dust'))
                            put(e['bundleQty'], 2, 7)
                            break
                        if 0 <= _switch287_index <= 1:
                            put(e['bundleItem'], 2, binary('+', binary('+', '<span class="book">', call(e['wikify'], 'Book Of Stars')), '</span>'))
                            break
                        if 0 <= _switch287_index <= 2:
                            put(e['bundleItem'], 2, binary('+', 'Next unshipped item<br/>OR<br/>', call(e['wikify'], 'Mystery Box')))
                            put(e['bundleQty'], 2, '1<br/>OR<br/>5')
                            break
                        if 0 <= _switch287_index <= 3:
                            put(e['bundleItem'], 2, call(e['wikify'], 'Stardrop Tea'))
                            break
                        if 0 <= _switch287_index <= 4:
                            put(e['bundleItem'], 2, 'Raccoon Seeds')
                            put(e['bundleQty'], 2, 25)
                            break
                        if 0 <= _switch287_index <= 5:
                            put(e['bundleItem'], 2, call(e['wikify'], 'Mystery Box'))
                            put(e['bundleQty'], 2, 3)
                            break
                        break
                break
            e.set('tclass', 'future')
            if truth(binary('===', e['timesFed'], get(e['save'], 'timesFedRaccoons'))):
                e.set('tclass', 'current')
            else:
                if truth(binary('<=', e['timesFed'], get(e['save'], 'timesFedRaccoons'))):
                    e.set('tclass', 'past')
            e.set('output', binary('+', e['output'], binary('+', binary('+', binary('+', binary('+', '<tr class="', e['tclass']), '"><td>'), call(e['addCommas'], e['tableRow'])), '</td>')))
            e.set('i', 0)
            while truth(binary('<', e['i'], 3)):
                if truth(get(e['isLong'], e['i'])):
                    if truth((binary('===', get(get(e['bundleItem'], e['i']), 0), get(get(e['bundleItem'], e['i']), 3)) if truth(_logic288 := (binary('===', get(get(e['bundleItem'], e['i']), 0), get(get(e['bundleItem'], e['i']), 2)) if truth(_logic289 := binary('===', get(get(e['bundleItem'], e['i']), 0), get(get(e['bundleItem'], e['i']), 1))) else _logic289)) else _logic288)):
                        e.set('output', binary('+', e['output'], binary('+', binary('+', binary('+', binary('+', '<td class="item">', get(get(e['bundleItem'], e['i']), 0)), '</td><td>'), get(e['bundleQty'], e['i'])), '</td>')))
                    else:
                        e.set('output', binary('+', e['output'], '<td class="item long_list">'))
                        e.set('s', 0)
                        while truth(binary('<', e['s'], 4)):
                            e.set('output', binary('+', e['output'], binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', '<img src="blank.png" class="season" id="sea_', e['s']), '" alt="'), get(get(e['save'], 'seasonNames'), e['s'])), '"> '), get(get(e['bundleItem'], e['i']), e['s'])), '<br/>')))
                            update_env(e, 's', 1, False)
                        e.set('output', binary('+', e['output'], binary('+', binary('+', '</td><td>', get(e['bundleQty'], e['i'])), '</td>')))
                else:
                    e.set('output', binary('+', e['output'], binary('+', binary('+', binary('+', binary('+', '<td class="item">', get(e['bundleItem'], e['i'])), '</td><td>'), get(e['bundleQty'], e['i'])), '</td>')))
                update_env(e, 'i', 1, False)
            e.set('output', binary('+', e['output'], '</tr>'))
            update_env(e, 'g', 1, False)
    e.set('output', binary('+', e['output'], '</tbody></table>'))
    return e['output']
    return U


def updateTab_290(parent, this, args):
    # Upstream predictor: 9084
    e = Env(parent)
    e.declare(['output'])
    e.local['arguments'] = Array(args)
    e.local['tabID'] = (args[0] if len(args) > 0 and args[0] is not U else U)
    e.local['isSearch'] = (args[1] if len(args) > 1 and args[1] is not U else U)
    e.local['offset'] = (args[2] if len(args) > 2 and args[2] is not U else U)
    e.local['extra'] = (args[3] if len(args) > 3 and args[3] is not U else U)
    e.set('output', '')
    if truth(binary('===', e['tabID'], 'mines')):
        e.set('output', call(e['predictMines'], e['isSearch'], e['offset']))
    else:
        if truth(binary('===', e['tabID'], 'cart')):
            e.set('output', call(e['predictCart'], e['isSearch'], e['offset']))
        else:
            if truth(binary('===', e['tabID'], 'geode')):
                e.set('output', call(e['predictGeodes'], e['isSearch'], e['offset']))
            else:
                if truth(binary('===', e['tabID'], 'mystery')):
                    e.set('output', call(e['predictMysteryBoxes'], e['isSearch'], e['offset']))
                else:
                    if truth(binary('===', e['tabID'], 'train')):
                        e.set('output', call(e['predictTrains'], e['isSearch'], e['offset']))
                    else:
                        if truth(binary('===', e['tabID'], 'night')):
                            e.set('output', call(e['predictNight'], e['isSearch'], e['offset']))
                        else:
                            if truth(binary('===', e['tabID'], 'crane')):
                                e.set('output', call(e['predictCrane'], e['isSearch'], e['offset']))
                            else:
                                if truth(binary('===', e['tabID'], 'krobus')):
                                    e.set('output', call(e['predictKrobus'], e['isSearch'], e['offset']))
                                else:
                                    if truth(binary('===', e['tabID'], 'sandy')):
                                        e.set('output', call(e['predictSandy'], e['isSearch'], e['offset']))
                                    else:
                                        if truth(binary('===', e['tabID'], 'wallpaper')):
                                            e.set('output', call(e['predictWallpaper'], e['isSearch'], e['offset']))
                                        else:
                                            if truth(binary('===', e['tabID'], 'trash')):
                                                e.set('output', call(e['predictTrash'], e['isSearch'], e['offset']))
                                            else:
                                                if truth(binary('===', e['tabID'], 'enchant')):
                                                    e.set('output', call(e['predictEnchantments'], e['isSearch'], e['offset']))
                                                else:
                                                    if truth(binary('===', e['tabID'], 'minechest')):
                                                        e.set('output', call(e['predictMineChests'], e['isSearch'], e['offset']))
                                                    else:
                                                        if truth(binary('===', e['tabID'], 'gembirds')):
                                                            e.set('output', call(e['predictGemBirds'], e['isSearch'], e['offset']))
                                                        else:
                                                            if truth(binary('===', e['tabID'], 'winterstar')):
                                                                e.set('output', call(e['predictWinterStar'], e['isSearch'], e['offset']))
                                                            else:
                                                                if truth(binary('===', e['tabID'], 'makeover')):
                                                                    e.set('output', call(e['predictMakeover'], e['isSearch'], e['offset']))
                                                                else:
                                                                    if truth(binary('===', e['tabID'], 'greenrain')):
                                                                        e.set('output', call(e['predictGreenRain'], e['isSearch'], e['offset']))
                                                                    else:
                                                                        if truth(binary('===', e['tabID'], 'cj')):
                                                                            e.set('output', call(e['predictCalicoJack'], e['isSearch'], e['offset'], e['extra']))
                                                                        else:
                                                                            if truth(binary('===', e['tabID'], 'book')):
                                                                                e.set('output', call(e['predictBookseller'], e['isSearch'], e['offset']))
                                                                            else:
                                                                                if truth(binary('===', e['tabID'], 'statue')):
                                                                                    e.set('output', call(e['predictStatues'], e['isSearch'], e['offset']))
                                                                                else:
                                                                                    if truth(binary('===', e['tabID'], 'prize')):
                                                                                        e.set('output', call(e['predictPrizeTicket'], e['isSearch'], e['offset']))
                                                                                    else:
                                                                                        if truth(binary('===', e['tabID'], 'raccoon')):
                                                                                            e.set('output', call(e['predictRaccoon'], e['isSearch'], e['offset']))
                                                                                        else:
                                                                                            call(get(e['console'], 'log'), binary('+', 'Unknown tabID: ', e['tabID']))
    put(call(get(e['document'], 'getElementById'), binary('+', 'out-', e['tabID'])), 'innerHTML', e['output'])
    return U

def create(environment):
    e = Env(environment)
    e.local["save"] = Obj()
    e.local['addCommas'] = Fn(addCommas_1, e)
    e.local['capitalize'] = Fn(capitalize_2, e)
    e.local['compareSemVer'] = Fn(compareSemVer_4, e)
    e.local['wikify'] = Fn(wikify_7, e)
    e.local['parseSummary'] = Fn(parseSummary_8, e)
    e.local['predictMines'] = Fn(predictMines_34, e)
    e.local['getRandomItemFromSeason'] = Fn(getRandomItemFromSeason_47, e)
    e.local['predictTrash'] = Fn(predictTrash_49, e)
    e.local['predictWallpaper'] = Fn(predictWallpaper_68, e)
    e.local['getCartItem'] = Fn(getCartItem_70, e)
    e.local['predictCart'] = Fn(predictCart_73, e)
    e.local['getRandomItems'] = Fn(getRandomItems_81, e)
    e.local['getRandomWallFloor'] = Fn(getRandomWallFloor_92, e)
    e.local['predictCart_1_6'] = Fn(predictCart_1_6_95, e)
    e.local['predictKrobus'] = Fn(predictKrobus_113, e)
    e.local['predictSandy'] = Fn(predictSandy_117, e)
    e.local['predictGeodes'] = Fn(predictGeodes_121, e)
    e.local['predictMysteryBoxes'] = Fn(predictMysteryBoxes_134, e)
    e.local['predictTrains'] = Fn(predictTrains_154, e)
    e.local['predictNight'] = Fn(predictNight_157, e)
    e.local['predictCrane'] = Fn(predictCrane_172, e)
    e.local['predictResortVisitors'] = Fn(predictResortVisitors_176, e)
    e.local['predictEnchantments'] = Fn(predictEnchantments_220, e)
    e.local['predictMineChests'] = Fn(predictMineChests_224, e)
    e.local['predictGemBirds'] = Fn(predictGemBirds_225, e)
    e.local['predictWinterStar'] = Fn(predictWinterStar_226, e)
    e.local['getNicerOutfitDescription'] = Fn(getNicerOutfitDescription_242, e)
    e.local['predictMakeover'] = Fn(predictMakeover_243, e)
    e.local['predictGreenRain'] = Fn(predictGreenRain_248, e)
    e.local['predictCalicoJack'] = Fn(predictCalicoJack_255, e)
    e.local['predictBookseller'] = Fn(predictBookseller_263, e)
    e.local['predictStatues'] = Fn(predictStatues_272, e)
    e.local['predictPrizeTicket'] = Fn(predictPrizeTicket_273, e)
    e.local['predictRaccoon'] = Fn(predictRaccoon_282, e)
    e.local['updateTab'] = Fn(updateTab_290, e)
    return e

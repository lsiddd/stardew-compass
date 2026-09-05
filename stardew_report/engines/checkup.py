# Python port of the pinned upstream calculation rules.
# Rules: MouseyPounds, MIT. Source locations accompany every function.
from ..runtime import *
from ..data import load_table

def table(index):
    return wrap(load_table('checkup', index))
def addCommas_1(parent, this, args):
    # Upstream checkup: 21
    e = Env(parent)
    e.declare([])
    e.local['arguments'] = Array(args)
    e.local['x'] = (args[0] if len(args) > 0 and args[0] is not U else U)
    return call(get(call(get(e['x'], 'toString')), 'replace'), Regex('\\B(?=(?:\\d{3})+(?!\\d))', 'g'), ',')
    return U


def capitalize_2(parent, this, args):
    # Upstream checkup: 26
    e = Env(parent)
    e.declare([])
    e.local['arguments'] = Array(args)
    e.local['s'] = (args[0] if len(args) > 0 and args[0] is not U else U)
    return (binary('+', call(get(get(e['s'], 0), 'toUpperCase')), call(get(e['s'], 'slice'), 1)) if truth(_logic3 := e['s']) else _logic3)
    return U


def compareSemVer_4(parent, this, args):
    # Upstream checkup: 31
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


def getAchieveString_7(parent, this, args):
    # Upstream checkup: 46
    e = Env(parent)
    e.declare([])
    e.local['arguments'] = Array(args)
    e.local['name'] = (args[0] if len(args) > 0 and args[0] is not U else U)
    e.local['desc'] = (args[1] if len(args) > 1 and args[1] is not U else U)
    e.local['yes'] = (args[2] if len(args) > 2 and args[2] is not U else U)
    if truth(binary('>', get(e['desc'], 'length'), 0)):
        e.set('desc', binary('+', binary('+', '(', e['desc']), ') '))
    return (binary('+', binary('+', binary('+', binary('+', '<span class="ach_yes"><span class="ach">', e['name']), '</span> '), e['desc']), ' achieved</span>') if truth(e['yes']) else binary('+', binary('+', binary('+', binary('+', '<span class="ach_no"><span class="ach">', e['name']), '</span> '), e['desc']), '</span> -- need '))
    return U


def getAchieveImpossibleString_8(parent, this, args):
    # Upstream checkup: 54
    e = Env(parent)
    e.declare([])
    e.local['arguments'] = Array(args)
    e.local['name'] = (args[0] if len(args) > 0 and args[0] is not U else U)
    e.local['desc'] = (args[1] if len(args) > 1 and args[1] is not U else U)
    if truth(binary('>', get(e['desc'], 'length'), 0)):
        e.set('desc', binary('+', binary('+', '(', e['desc']), ') '))
    return binary('+', binary('+', binary('+', binary('+', '<span class="ach_imp"><span class="ach">', e['name']), '</span> '), e['desc']), ' impossible</span>')
    return U


def getMilestoneString_9(parent, this, args):
    # Upstream checkup: 61
    e = Env(parent)
    e.declare([])
    e.local['arguments'] = Array(args)
    e.local['desc'] = (args[0] if len(args) > 0 and args[0] is not U else U)
    e.local['yes'] = (args[1] if len(args) > 1 and args[1] is not U else U)
    return (binary('+', binary('+', '<span class="ms_yes">', e['desc']), '</span>') if truth(e['yes']) else binary('+', binary('+', '<span class="ms_no">', e['desc']), '</span> -- need '))
    return U


def getPointString_10(parent, this, args):
    # Upstream checkup: 66
    e = Env(parent)
    e.declare(['c'])
    e.local['arguments'] = Array(args)
    e.local['pts'] = (args[0] if len(args) > 0 and args[0] is not U else U)
    e.local['desc'] = (args[1] if len(args) > 1 and args[1] is not U else U)
    e.local['cum'] = (args[2] if len(args) > 2 and args[2] is not U else U)
    e.local['yes'] = (args[3] if len(args) > 3 and args[3] is not U else U)
    e.set('c', (' more' if truth(e['cum']) else ''))
    return (binary('+', binary('+', binary('+', binary('+', binary('+', '<span class="pt_yes"><span class="pts">+', e['pts']), e['c']), '</span> earned ('), e['desc']), ')</span>') if truth(e['yes']) else binary('+', binary('+', binary('+', binary('+', binary('+', '<span class="pt_no"><span class="pts"> (', e['pts']), e['c']), ')</span> possible ('), e['desc']), ')</span>'))
    return U


def getPointImpossibleString_11(parent, this, args):
    # Upstream checkup: 72
    e = Env(parent)
    e.declare([])
    e.local['arguments'] = Array(args)
    e.local['pts'] = (args[0] if len(args) > 0 and args[0] is not U else U)
    e.local['desc'] = (args[1] if len(args) > 1 and args[1] is not U else U)
    return binary('+', binary('+', binary('+', binary('+', '<span class="pt_imp"><span class="pts">+', e['pts']), '</span> impossible ('), e['desc']), ')</span>')
    return U


def getPerfectionPctString_12(parent, this, args):
    # Upstream checkup: 76
    e = Env(parent)
    e.declare(['extra', 'places', 'pretty_pct', 'pts'])
    e.local['arguments'] = Array(args)
    e.local['pct'] = (args[0] if len(args) > 0 and args[0] is not U else U)
    e.local['max'] = (args[1] if len(args) > 1 and args[1] is not U else U)
    e.local['desc'] = (args[2] if len(args) > 2 and args[2] is not U else U)
    e.local['yes'] = (args[3] if len(args) > 3 and args[3] is not U else U)
    e.local['who'] = (args[4] if len(args) > 4 and args[4] is not U else '')
    e.set('pts', binary('*', e['max'], e['pct']))
    e.set('places', 2)
    e.set('extra', ('' if truth(binary('===', e['who'], '')) else ('' if truth(binary('===', e['pct'], 0)) else binary('+', ' thanks to ', e['who']))))
    if truth((_logic13 if truth(_logic13 := binary('<', e['pct'], 0.0001)) else binary('>', e['pct'], 0.9999))):
        e.set('places', 0)
    e.set('pts', call(get(e['pts'], 'toFixed'), e['places']))
    e.set('pretty_pct', binary('*', 100, e['pct']))
    e.set('pretty_pct', call(get(e['pretty_pct'], 'toFixed'), call(get(e['Math'], 'max'), 0, binary('-', e['places'], 1))))
    return (binary('+', binary('+', binary('+', binary('+', binary('+', '<span class="pt_yes"><span class="pts">', e['pts']), '%</span> from completion of '), e['desc']), e['extra']), '</span>') if truth(e['yes']) else binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', '<span class="pt_no"><span class="pts"> ', e['pts']), '%</span> (of '), e['max']), '% possible) from '), e['desc']), e['extra']), ' ('), e['pretty_pct']), '%)</span>'))
    return U


def getPerfectionNumString_14(parent, this, args):
    # Upstream checkup: 89
    e = Env(parent)
    e.declare(['extra', 'pretty_pct', 'pts'])
    e.local['arguments'] = Array(args)
    e.local['num'] = (args[0] if len(args) > 0 and args[0] is not U else U)
    e.local['max'] = (args[1] if len(args) > 1 and args[1] is not U else U)
    e.local['desc'] = (args[2] if len(args) > 2 and args[2] is not U else U)
    e.local['yes'] = (args[3] if len(args) > 3 and args[3] is not U else U)
    e.local['who'] = (args[4] if len(args) > 4 and args[4] is not U else '')
    e.set('pts', e['num'])
    e.set('pretty_pct', binary('+', binary('+', e['num'], '/'), e['max']))
    e.set('extra', ('' if truth(binary('===', e['who'], '')) else ('' if truth(binary('===', e['num'], 0)) else binary('+', ' thanks to ', e['who']))))
    return (binary('+', binary('+', binary('+', binary('+', binary('+', '<span class="pt_yes"><span class="pts">', e['pts']), '%</span> from completion of '), e['desc']), e['extra']), '</span>') if truth(e['yes']) else binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', '<span class="pt_no"><span class="pts"> ', e['pts']), '%</span> (of '), e['max']), '% possible) from '), e['desc']), e['extra']), ' ('), e['pretty_pct']), ')</span>'))
    return U


def getPerfectionPctNumString_15(parent, this, args):
    # Upstream checkup: 98
    e = Env(parent)
    e.declare(['extra', 'places', 'pretty_pct', 'pts'])
    e.local['arguments'] = Array(args)
    e.local['pct'] = (args[0] if len(args) > 0 and args[0] is not U else U)
    e.local['max'] = (args[1] if len(args) > 1 and args[1] is not U else U)
    e.local['count'] = (args[2] if len(args) > 2 and args[2] is not U else U)
    e.local['desc'] = (args[3] if len(args) > 3 and args[3] is not U else U)
    e.local['yes'] = (args[4] if len(args) > 4 and args[4] is not U else U)
    e.local['who'] = (args[5] if len(args) > 5 and args[5] is not U else '')
    e.set('pts', binary('*', e['max'], e['pct']))
    e.set('places', 2)
    e.set('extra', ('' if truth(binary('===', e['who'], '')) else ('' if truth(binary('===', e['pct'], 0)) else binary('+', ' thanks to ', e['who']))))
    if truth((_logic16 if truth(_logic16 := binary('<', e['pct'], 0.0001)) else binary('>', e['pct'], 0.9999))):
        e.set('places', 0)
    e.set('pts', call(get(e['pts'], 'toFixed'), e['places']))
    e.set('pretty_pct', binary('+', binary('+', binary('+', binary('+', binary('+', call(get(e['Math'], 'round'), binary('*', e['count'], e['pct'])), '/'), e['count']), ' or '), call(get(call(e['Number'], binary('*', 100, e['pct'])), 'toFixed'), call(get(e['Math'], 'max'), 0, binary('-', e['places'], 1)))), '%'))
    return (binary('+', binary('+', binary('+', binary('+', binary('+', '<span class="pt_yes"><span class="pts">', e['pts']), '%</span> from completion of '), e['desc']), e['extra']), '</span>') if truth(e['yes']) else binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', '<span class="pt_no"><span class="pts"> ', e['pts']), '%</span> (of '), e['max']), '% possible) from '), e['desc']), e['extra']), ' ('), e['pretty_pct']), ')</span>'))
    return U


def getPerfectionBoolString_17(parent, this, args):
    # Upstream checkup: 110
    e = Env(parent)
    e.declare(['extra'])
    e.local['arguments'] = Array(args)
    e.local['max'] = (args[0] if len(args) > 0 and args[0] is not U else U)
    e.local['desc'] = (args[1] if len(args) > 1 and args[1] is not U else U)
    e.local['yes'] = (args[2] if len(args) > 2 and args[2] is not U else U)
    e.local['who'] = (args[3] if len(args) > 3 and args[3] is not U else '')
    e.set('extra', ('' if truth(binary('===', e['who'], '')) else binary('+', ' thanks to ', e['who'])))
    return (binary('+', binary('+', binary('+', binary('+', binary('+', '<span class="pt_yes"><span class="pts">', e['max']), '%</span> from completion of '), e['desc']), e['extra']), '</span>') if truth(e['yes']) else binary('+', binary('+', binary('+', binary('+', '<span class="pt_no"><span class="pts"> 0%</span> (of ', e['max']), '% possible) from '), e['desc']), '</span>'))
    return U


def wikify_18(parent, this, args):
    # Upstream checkup: 116
    e = Env(parent)
    e.declare(['trimmed'])
    e.local['arguments'] = Array(args)
    e.local['item'] = (args[0] if len(args) > 0 and args[0] is not U else U)
    e.local['page'] = (args[1] if len(args) > 1 and args[1] is not U else U)
    e.local['no_anchor'] = (args[2] if len(args) > 2 and args[2] is not U else U)
    e.set('trimmed', call(get(e['item'], 'replace'), ' (White)', ''))
    e.set('trimmed', call(get(e['trimmed'], 'replace'), ' (Brown)', ''))
    e.set('trimmed', call(get(e['trimmed'], 'replace'), ' (Any)', ''))
    e.set('trimmed', call(get(e['trimmed'], 'replace'), Regex('#', 'g'), '.23'))
    e.set('trimmed', call(get(e['trimmed'], 'replace'), Regex(' ', 'g'), '_'))
    if truth(e['page']):
        return (binary('+', binary('+', binary('+', binary('+', '<a href="https://stardewvalleywiki.com/', e['page']), '">'), e['item']), '</a>') if truth(e['no_anchor']) else binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', '<a href="https://stardewvalleywiki.com/', e['page']), '#'), e['trimmed']), '">'), e['item']), '</a>'))
    else:
        return binary('+', binary('+', binary('+', binary('+', '<a href="https://stardewvalleywiki.com/', e['trimmed']), '">'), e['item']), '</a>')
    return U


def wikimap_19(parent, this, args):
    # Upstream checkup: 131
    e = Env(parent)
    e.declare([])
    e.local['arguments'] = Array(args)
    e.local['item'] = (args[0] if len(args) > 0 and args[0] is not U else U)
    e.local['index'] = (args[1] if len(args) > 1 and args[1] is not U else U)
    e.local['arr'] = (args[2] if len(args) > 2 and args[2] is not U else U)
    return call(e['wikify'], e['item'])
    return U


def printTranspose_20(parent, this, args):
    # Upstream checkup: 136
    e = Env(parent)
    e.declare(['c', 'id', 'output', 'r'])
    e.local['arguments'] = Array(args)
    e.local['table'] = (args[0] if len(args) > 0 and args[0] is not U else U)
    e.set('output', '<table class="output">')
    e.set('r', 0)
    while truth(binary('<', e['r'], get(get(e['table'], 0), 'length'))):
        e.set('output', binary('+', e['output'], '<tr>'))
        e.set('c', 0)
        while truth(binary('<', e['c'], get(e['table'], 'length'))):
            e.set('id', binary('+', 'PL_', binary('+', e['c'], 1)))
            e.set('output', binary('+', e['output'], binary('+', binary('+', binary('+', binary('+', '<td class="', e['id']), '">'), get(get(e['table'], e['c']), e['r'])), '</td>')))
            update_env(e, 'c', 1, False)
        e.set('output', binary('+', e['output'], '</tr>'))
        update_env(e, 'r', 1, False)
    e.set('output', binary('+', e['output'], '</table>'))
    return e['output']
    return U


def isValidFarmhand_21(parent, this, args):
    # Upstream checkup: 151
    e = Env(parent)
    e.declare([])
    e.local['arguments'] = Array(args)
    e.local['player'] = (args[0] if len(args) > 0 and args[0] is not U else U)
    if truth((binary('===', call(get(call(get(call(e['$'], e['player']), 'children'), 'name'), 'text')), '') if truth(_logic22 := binary('===', call(get(call(get(call(e['$'], e['player']), 'children'), 'userID'), 'text')), '')) else _logic22)):
        return False
    return True
    return U


def getSummaryClass_23(parent, this, args):
    # Upstream checkup: 161
    e = Env(parent)
    e.declare(['prefs', 'sum_class'])
    e.local['arguments'] = Array(args)
    e.local['saveInfo'] = (args[0] if len(args) > 0 and args[0] is not U else U)
    e.local['version'] = (args[1] if len(args) > 1 and args[1] is not U else U)
    e.set('prefs', (get(e['saveInfo'], 'outputPrefOld') if truth(binary('<', call(e['compareSemVer'], e['version'], '1.6'), 0)) else get(e['saveInfo'], 'outputPrefNew')))
    e.set('sum_class', 'initial_hide')
    if truth((_logic24 if truth(_logic24 := binary('===', e['prefs'], 'show_all')) else binary('===', e['prefs'], 'hide_details'))):
        e.set('sum_class', 'initial_show')
    return e['sum_class']
    return U


def getDetailsClass_25(parent, this, args):
    # Upstream checkup: 171
    e = Env(parent)
    e.declare(['det_class', 'prefs'])
    e.local['arguments'] = Array(args)
    e.local['saveInfo'] = (args[0] if len(args) > 0 and args[0] is not U else U)
    e.local['version'] = (args[1] if len(args) > 1 and args[1] is not U else U)
    e.set('prefs', (get(e['saveInfo'], 'outputPrefOld') if truth(binary('<', call(e['compareSemVer'], e['version'], '1.6'), 0)) else get(e['saveInfo'], 'outputPrefNew')))
    e.set('det_class', 'initial_show')
    if truth((_logic26 if truth(_logic26 := binary('===', e['prefs'], 'hide_all')) else binary('===', e['prefs'], 'hide_details'))):
        e.set('det_class', 'initial_hide')
    return e['det_class']
    return U


def getPTLink_27(parent, this, args):
    # Upstream checkup: 181
    e = Env(parent)
    e.declare(['n', 'places'])
    e.local['arguments'] = Array(args)
    e.local['input'] = (args[0] if len(args) > 0 and args[0] is not U else U)
    e.local['isPct'] = (args[1] if len(args) > 1 and args[1] is not U else U)
    if truth(e['isPct']):
        e.set('places', (0 if truth(binary('===', e['input'], 1)) else 1))
        e.set('n', call(get(call(e['Number'], binary('*', 100, e['input'])), 'toFixed'), e['places']))
        e.set('input', binary('+', e['n'], '%'))
    return binary('+', binary('+', ' (<a href="#sec_Perfection_Tracker">PT: ', e['input']), '</a>)')
    return U


def getSectionHeader_28(parent, this, args):
    # Upstream checkup: 193
    e = Env(parent)
    e.declare(['button_element', 'det_button', 'det_class', 'output', 'prefs', 'sum_button', 'sum_class'])
    e.local['arguments'] = Array(args)
    e.local['saveInfo'] = (args[0] if len(args) > 0 and args[0] is not U else U)
    e.local['title'] = (args[1] if len(args) > 1 and args[1] is not U else U)
    e.local['anchor'] = (args[2] if len(args) > 2 and args[2] is not U else U)
    e.local['showDetailsButton'] = (args[3] if len(args) > 3 and args[3] is not U else U)
    e.local['version'] = (args[4] if len(args) > 4 and args[4] is not U else U)
    e.set('prefs', (get(e['saveInfo'], 'outputPrefOld') if truth(binary('<', call(e['compareSemVer'], e['version'], '1.6'), 0)) else get(e['saveInfo'], 'outputPrefNew')))
    e.set('output', binary('+', binary('+', binary('+', binary('+', '<div class="collapsible" id="wrap_', e['anchor']), '"><h3>'), e['title']), '</h3>'))
    if truth((_logic29 if truth(_logic29 := binary('===', e['prefs'], 'show_all')) else binary('===', e['prefs'], 'hide_details'))):
        e.set('sum_button', 'Hide Summary')
    else:
        e.set('sum_button', 'Show Summary')
    if truth((_logic30 if truth(_logic30 := binary('===', e['prefs'], 'hide_all')) else binary('===', e['prefs'], 'hide_details'))):
        e.set('det_button', 'Show Details')
    else:
        e.set('det_button', 'Hide Details')
    e.set('button_element', '(No Details)')
    if truth(e['showDetailsButton']):
        e.set('button_element', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', '<button id="toggle_', e['anchor']), '_details" type="button" data-target="'), e['anchor']), '_details">'), e['det_button']), '</button>'))
    e.set('output', binary('+', e['output'], binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', ' <button id="toggle_', e['anchor']), '_summary" type="button" data-target="'), e['anchor']), '_summary">'), e['sum_button']), '</button> '), e['button_element'])))
    return e['output']
    return U


def getSectionFooter_31(parent, this, args):
    # Upstream checkup: 225
    e = Env(parent)
    e.declare([])
    e.local['arguments'] = Array(args)
    return '</div>'
    return U


def collapsibleWrap_32(parent, this, args):
    # Upstream checkup: 231
    e = Env(parent)
    e.declare([])
    e.local['arguments'] = Array(args)
    e.local['saveInfo'] = (args[0] if len(args) > 0 and args[0] is not U else U)
    e.local['title'] = (args[1] if len(args) > 1 and args[1] is not U else U)
    e.local['output'] = (args[2] if len(args) > 2 and args[2] is not U else U)
    e.local['version'] = (args[3] if len(args) > 3 and args[3] is not U else U)
    return binary('+', '<h4>PLACEHOLDER</h4>', e['output'])
    return U


def makeAnchor_33(parent, this, args):
    # Upstream checkup: 233
    e = Env(parent)
    e.declare(['id'])
    e.local['arguments'] = Array(args)
    e.local['text'] = (args[0] if len(args) > 0 and args[0] is not U else U)
    e.set('id', e['text'])
    call(get(e['id'], 'toLowerCase'))
    return call(get(e['id'], 'replace'), Regex('[^\\w*]', 'g'), '_')
    return U


def callback_35(parent, this, args):
    # Upstream checkup: 302
    e = Env(parent)
    e.declare([])
    e.local['arguments'] = Array(args)
    call(get(get(get(e['saveInfo'], 'children'), e['id']), 'push'), call(get(call(get(call(e['$'], this), 'find'), 'name'), 'html')))
    return U


def callback_36(parent, this, args):
    # Upstream checkup: 327
    e = Env(parent)
    e.declare(['id'])
    e.local['arguments'] = Array(args)
    if truth(call(e['isValidFarmhand'], this)):
        update_prop(e['saveInfo'], 'numPlayers', 1, False)
        e.set('id', call(e['populateData'], call(e['$'], this), e['saveInfo']))
        call(get(e['farmhands'], 'push'), get(get(get(e['saveInfo'], 'data'), e['id']), 'name'))
        put(get(e['saveInfo'], 'players'), e['id'], get(get(get(e['saveInfo'], 'data'), e['id']), 'name'))
        put(get(e['saveInfo'], 'children'), e['id'], Array([]))
        put(get(e['saveInfo'], 'perfectionTracker'), e['id'], Obj({}))
    return U


def callback_37(parent, this, args):
    # Upstream checkup: 339
    e = Env(parent)
    e.declare([])
    e.local['arguments'] = Array(args)
    e.set('id', call(get(call(get(call(e['$'], this), 'children'), 'idOfParent'), 'text')))
    call(get(get(get(e['saveInfo'], 'children'), e['id']), 'push'), call(get(call(get(call(e['$'], this), 'find'), 'name'), 'html')))
    return U


def callback_38(parent, this, args):
    # Upstream checkup: 350
    e = Env(parent)
    e.declare(['id1', 'id2', 'item'])
    e.local['arguments'] = Array(args)
    e.set('item', this)
    if truth(binary('===', call(get(call(get(call(e['$'], this), 'find'), 'value > Friendship > Status'), 'text')), 'Married')):
        e.set('id1', call(get(call(get(call(e['$'], e['item']), 'find'), 'key > FarmerPair > Farmer1'), 'text')))
        e.set('id2', call(get(call(get(call(e['$'], e['item']), 'find'), 'key > FarmerPair > Farmer2'), 'text')))
        put(get(e['saveInfo'], 'partners'), e['id1'], e['id2'])
        put(get(e['saveInfo'], 'partners'), e['id2'], e['id1'])
    return U


def parseSummary_34(parent, this, args):
    # Upstream checkup: 246
    e = Env(parent)
    e.declare(['anchor', 'details', 'farmTypes', 'farmer', 'farmhandSelector', 'farmhands', 'id', 'output', 'playHr', 'playMin', 'playTime', 'sum_class', 'title', 'version', 'versionLabel'])
    e.local['arguments'] = Array(args)
    e.local['xmlDoc'] = (args[0] if len(args) > 0 and args[0] is not U else U)
    e.local['saveInfo'] = (args[1] if len(args) > 1 and args[1] is not U else U)
    e.set('title', 'Summary')
    e.set('anchor', call(e['makeAnchor'], e['title']))
    e.set('version', '1.2')
    e.set('sum_class', call(e['getSummaryClass'], e['saveInfo'], e['version']))
    e.set('output', '')
    e.set('details', '')
    e.set('farmTypes', Obj({'0': 'Standard', '1': 'Riverland', '2': 'Forest', '3': 'Hill-top', '4': 'Wilderness', '5': 'Four Corners', '6': 'Beach', 'MeadowlandsFarm': 'Meadowlands'}))
    e.set('playTime', call(e['Number'], call(get(call(get(call(e['$'], e['xmlDoc']), 'find'), 'player > millisecondsPlayed'), 'text'))))
    e.set('playHr', call(get(e['Math'], 'floor'), binary('/', e['playTime'], 3600000)))
    e.set('playMin', call(get(e['Math'], 'floor'), binary('/', binary('%', e['playTime'], 3600000), 60000)))
    e.set('id', '0')
    e.set('farmhands', Array([]))
    e.set('farmhandSelector', 'farmhand')
    put(e['saveInfo'], 'version', call(get(call(get(call(get(call(e['$'], e['xmlDoc']), 'find'), 'gameVersion'), 'first')), 'text')))
    if truth(binary('===', get(e['saveInfo'], 'version'), '')):
        put(e['saveInfo'], 'version', '1.2')
        if truth(binary('===', call(get(call(get(call(e['$'], e['xmlDoc']), 'find'), 'hasApplied1_4_UpdateChanges'), 'text')), 'true')):
            put(e['saveInfo'], 'version', '1.4')
        else:
            if truth(binary('===', call(get(call(get(call(e['$'], e['xmlDoc']), 'find'), 'hasApplied1_3_UpdateChanges'), 'text')), 'true')):
                put(e['saveInfo'], 'version', '1.3')
    e.set('versionLabel', call(get(call(get(call(get(call(e['$'], e['xmlDoc']), 'find'), 'gameVersionLabel'), 'first')), 'text')))
    if truth(binary('===', e['versionLabel'], '')):
        put(e['saveInfo'], 'versionLabel', '')
    else:
        put(e['saveInfo'], 'versionLabel', binary('+', binary('+', '(', e['versionLabel']), ')'))
    put(e['saveInfo'], 'ns_prefix', ('xsi' if truth(binary('>', get(call(get(call(e['$'], e['xmlDoc']), 'find'), 'SaveGame[xmlns\\:xsi]'), 'length'), 0)) else 'p3'))
    put(e['saveInfo'], 'players', Obj({}))
    put(e['saveInfo'], 'children', Obj({}))
    put(e['saveInfo'], 'data', Obj({}))
    e.set('id', call(e['populateData'], call(get(call(e['$'], e['xmlDoc']), 'find'), 'player'), e['saveInfo']))
    put(e['saveInfo'], 'farmerId', e['id'])
    e.set('farmer', get(get(get(e['saveInfo'], 'data'), e['id']), 'name'))
    put(get(e['saveInfo'], 'players'), e['id'], get(get(get(e['saveInfo'], 'data'), e['id']), 'name'))
    put(get(e['saveInfo'], 'children'), e['id'], Array([]))
    call(get(call(get(call(e['$'], e['xmlDoc']), 'find'), binary('+', binary('+', binary('+', binary('+', '[', get(e['saveInfo'], 'ns_prefix')), "\\:type='FarmHouse'] NPC["), get(e['saveInfo'], 'ns_prefix')), "\\:type='Child']")), 'each'), Fn(callback_35, e))
    put(e['saveInfo'], 'numPlayers', 1)
    put(e['saveInfo'], 'farmName', call(get(call(get(call(e['$'], e['xmlDoc']), 'find'), 'player > farmName'), 'html')))
    put(e['saveInfo'], 'perfectionTracker', table(0))
    put(get(e['saveInfo'], 'perfectionTracker'), e['id'], Obj({}))
    e.set('output', call(e['getSectionHeader'], e['saveInfo'], e['title'], e['anchor'], False, e['version']))
    e.set('output', binary('+', e['output'], binary('+', binary('+', binary('+', binary('+', '<div class="', e['anchor']), '_summary '), e['sum_class']), '">')))
    e.set('output', binary('+', e['output'], binary('+', binary('+', binary('+', binary('+', '<span class="result">', get(e['saveInfo'], 'farmName')), ' Farm ('), get(e['farmTypes'], call(get(call(get(call(e['$'], e['xmlDoc']), 'find'), 'whichFarm'), 'text')))), ')</span><br />')))
    e.set('output', binary('+', e['output'], binary('+', '<span class="result">Farmer ', e['farmer'])))
    if truth(binary('>=', call(e['compareSemVer'], get(e['saveInfo'], 'version'), '1.6'), 0)):
        e.set('farmhandSelector', 'farmhands > Farmer')
    call(get(call(get(call(e['$'], e['xmlDoc']), 'find'), e['farmhandSelector']), 'each'), Fn(callback_36, e))
    call(get(call(get(call(get(call(e['$'], e['xmlDoc']), 'find'), binary('+', binary('+', 'indoors[', get(e['saveInfo'], 'ns_prefix')), '\\:type="Cabin"]')), 'find'), binary('+', binary('+', 'NPC[', get(e['saveInfo'], 'ns_prefix')), "\\:type='Child']")), 'each'), Fn(callback_37, e))
    if truth(binary('>', get(e['saveInfo'], 'numPlayers'), 1)):
        e.set('output', binary('+', e['output'], binary('+', ' and Farmhand(s) ', call(get(e['farmhands'], 'join'), ', '))))
        call(e['createPlayerList'], get(e['saveInfo'], 'numPlayers'), e['farmer'], e['farmhands'])
    e.set('output', binary('+', e['output'], '</span><br />'))
    put(e['saveInfo'], 'partners', Obj({}))
    call(get(call(get(call(e['$'], e['xmlDoc']), 'find'), 'farmerFriendships > item'), 'each'), Fn(callback_38, e))
    put(e['saveInfo'], 'objects', table(1))
    e.set('output', binary('+', e['output'], binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', '<span class="result">Day ', call(e['Number'], call(get(call(get(call(e['$'], e['xmlDoc']), 'find'), 'dayOfMonth'), 'text')))), ' of '), call(e['capitalize'], call(get(call(get(call(e['$'], e['xmlDoc']), 'find'), 'currentSeason'), 'html')))), ', Year '), call(e['Number'], call(get(call(get(call(e['$'], e['xmlDoc']), 'find'), 'year'), 'text')))), '</span><br />')))
    e.set('output', binary('+', e['output'], '<span class="result">Played for '))
    if truth((binary('===', e['playMin'], 0) if truth(_logic39 := binary('===', e['playHr'], 0)) else _logic39)):
        e.set('output', binary('+', e['output'], 'less than 1 minute'))
    else:
        if truth(binary('>', e['playHr'], 0)):
            e.set('output', binary('+', e['output'], binary('+', e['playHr'], ' hr ')))
        if truth(binary('>', e['playMin'], 0)):
            e.set('output', binary('+', e['output'], binary('+', e['playMin'], ' min ')))
    e.set('output', binary('+', e['output'], '</span><br />'))
    e.set('output', binary('+', e['output'], binary('+', binary('+', binary('+', binary('+', '<span class="result">Save is from version ', get(e['saveInfo'], 'version')), ' '), get(e['saveInfo'], 'versionLabel')), '</span><br /></div>')))
    e.set('output', binary('+', e['output'], call(e['getSectionFooter'])))
    return e['output']
    return U


def callback_41(parent, this, args):
    # Upstream checkup: 1016
    e = Env(parent)
    e.declare([])
    e.local['arguments'] = Array(args)
    if truth(call(e['isValidFarmhand'], this)):
        call(get(e['table'], 'push'), call(e['func'], this, e['saveInfo'], *e['args']))
    return U


def parseFarmhands_40(parent, this, args):
    # Upstream checkup: 1010
    e = Env(parent)
    e.declare(['farmhandSelector'])
    e.local['arguments'] = Array(args)
    e.local['xmlDoc'] = (args[0] if len(args) > 0 and args[0] is not U else U)
    e.local['saveInfo'] = (args[1] if len(args) > 1 and args[1] is not U else U)
    e.local['table'] = (args[2] if len(args) > 2 and args[2] is not U else U)
    e.local['func'] = (args[3] if len(args) > 3 and args[3] is not U else U)
    e.local['args'] = Array(args[4:])
    if truth(binary('>', get(e['saveInfo'], 'numPlayers'), 1)):
        e.set('farmhandSelector', 'farmhand')
        if truth(binary('>=', call(e['compareSemVer'], get(e['saveInfo'], 'version'), '1.6'), 0)):
            e.set('farmhandSelector', 'farmhands > Farmer')
        call(get(call(get(call(e['$'], e['xmlDoc']), 'find'), e['farmhandSelector']), 'each'), Fn(callback_41, e))
    return U


def callback_43(parent, this, args):
    # Upstream checkup: 1047
    e = Env(parent)
    e.declare(['key', 'value'])
    e.local['arguments'] = Array(args)
    if truth(e['newStatFormat']):
        e.set('key', call(get(call(get(call(e['$'], this), 'find'), 'key > string'), 'text')))
        e.set('value', call(get(call(get(call(e['$'], this), 'find'), 'value > *'), 'text')))
    else:
        e.set('key', get(get(call(e['$'], this), 0), 'nodeName'))
        e.set('value', call(get(call(e['$'], this), 'text')))
    put(get(get(get(e['saveInfo'], 'data'), e['id']), 'stats'), e['key'], e['value'])
    return U


def callback_44(parent, this, args):
    # Upstream checkup: 1059
    e = Env(parent)
    e.declare([])
    e.local['arguments'] = Array(args)
    put(get(get(get(e['saveInfo'], 'data'), e['id']), 'mailReceived'), call(get(call(e['$'], this), 'text')), True)
    return U


def callback_45(parent, this, args):
    # Upstream checkup: 1063
    e = Env(parent)
    e.declare([])
    e.local['arguments'] = Array(args)
    put(get(get(get(e['saveInfo'], 'data'), e['id']), 'eventsSeen'), call(get(call(e['$'], this), 'text')), True)
    return U


def callback_46(parent, this, args):
    # Upstream checkup: 1067
    e = Env(parent)
    e.declare([])
    e.local['arguments'] = Array(args)
    call(get(get(get(get(e['saveInfo'], 'data'), e['id']), 'experiencePoints'), 'push'), call(e['Number'], call(get(call(e['$'], this), 'text'))))
    return U


def callback_47(parent, this, args):
    # Upstream checkup: 1073
    e = Env(parent)
    e.declare(['key', 'value'])
    e.local['arguments'] = Array(args)
    e.set('key', call(e['Number'], call(get(call(get(call(e['$'], this), 'find'), 'key > int'), 'text'))))
    e.set('value', call(get(call(get(call(e['$'], this), 'find'), 'value > *'), 'text')))
    put(get(get(get(e['saveInfo'], 'data'), e['id']), 'chestConsumedMineLevels'), e['key'], e['value'])
    return U


def populateData_42(parent, this, args):
    # Upstream checkup: 1024
    e = Env(parent)
    e.declare(['id', 'name', 'newStatFormat', 'selector', 'statBase'])
    e.local['arguments'] = Array(args)
    e.local['player'] = (args[0] if len(args) > 0 and args[0] is not U else U)
    e.local['saveInfo'] = (args[1] if len(args) > 1 and args[1] is not U else U)
    e.set('id', '0')
    e.set('name', call(get(call(get(call(e['$'], e['player']), 'children'), 'name'), 'html')))
    if truth(binary('>=', call(e['compareSemVer'], get(e['saveInfo'], 'version'), '1.3'), 0)):
        e.set('id', call(get(call(get(call(e['$'], e['player']), 'children'), 'UniqueMultiplayerID'), 'text')))
        try:
            if truth(binary('===', binary('%', call(e['BigInt'], e['id']), call(e['BigInt'], 111)), 0)):
                call(get(e['console'], 'log'), binary('+', binary('+', 'Player ', e['name']), ' is bad at music'))
        except Exception as _error:
            e.local['e'] = str(_error)
            call(get(e['console'], 'log'), "Browser doesn't support BigInt so skipped the bad at music check.")
    put(get(e['saveInfo'], 'data'), e['id'], Obj({}))
    put(get(get(e['saveInfo'], 'data'), e['id']), 'name', e['name'])
    put(get(get(e['saveInfo'], 'data'), e['id']), 'umid', e['id'])
    put(get(get(e['saveInfo'], 'data'), e['id']), 'stats', Obj({}))
    e.set('newStatFormat', binary('>=', call(e['compareSemVer'], get(e['saveInfo'], 'version'), '1.6'), 0))
    e.set('selector', ('stats > Values > item' if truth(e['newStatFormat']) else 'stats > *'))
    e.set('statBase', (e['player'] if truth(binary('>=', call(e['compareSemVer'], get(e['saveInfo'], 'version'), '1.3'), 0)) else call(get(call(e['$'], e['player']), 'parent'))))
    call(get(call(get(call(e['$'], e['statBase']), 'find'), e['selector']), 'each'), Fn(callback_43, e))
    put(get(get(e['saveInfo'], 'data'), e['id']), 'mailReceived', Obj({}))
    call(get(call(get(call(e['$'], e['player']), 'find'), 'mailReceived > string'), 'each'), Fn(callback_44, e))
    put(get(get(e['saveInfo'], 'data'), e['id']), 'eventsSeen', Obj({}))
    call(get(call(get(call(e['$'], e['player']), 'find'), 'eventsSeen > *'), 'each'), Fn(callback_45, e))
    put(get(get(e['saveInfo'], 'data'), e['id']), 'experiencePoints', Array([]))
    call(get(call(get(call(e['$'], e['player']), 'find'), 'experiencePoints > int'), 'each'), Fn(callback_46, e))
    put(get(get(e['saveInfo'], 'data'), e['id']), 'chestConsumedMineLevels', Obj({}))
    call(get(call(get(call(e['$'], e['player']), 'find'), 'chestConsumedLevels > item'), 'each'), Fn(callback_47, e))
    put(get(get(e['saveInfo'], 'data'), e['id']), 'maxStamina', call(e['Number'], call(get(call(get(call(e['$'], e['player']), 'find'), 'maxStamina'), 'text'))))
    return e['id']
    return U


def callback_49(parent, this, args):
    # Upstream checkup: 1122
    e = Env(parent)
    e.declare(['m'])
    e.local['arguments'] = Array(args)
    e.local['id'] = (args[0] if len(args) > 0 and args[0] is not U else U)
    e.set('m', (_logic50 if truth(_logic50 := get(get(get(get(e['saveInfo'], 'data'), e['id']), 'stats'), 'individualMoneyEarned')) else 0))
    e.set('output', binary('+', e['output'], binary('+', binary('+', binary('+', binary('+', '<li>', call(e['addCommas'], e['m'])), 'g earned by '), get(get(e['saveInfo'], 'players'), e['id'])), '</li>')))
    e.set('left', binary('-', e['left'], e['m']))
    return U


def parseMoney_48(parent, this, args):
    # Upstream checkup: 1083
    e = Env(parent)
    e.declare(['anchor', 'det_class', 'left', 'meta', 'money', 'output', 'playerOutput', 'separateWallets', 'sum_class', 'table', 'title', 'version'])
    e.local['arguments'] = Array(args)
    e.local['xmlDoc'] = (args[0] if len(args) > 0 and args[0] is not U else U)
    e.local['saveInfo'] = (args[1] if len(args) > 1 and args[1] is not U else U)
    e.set('title', 'Money')
    e.set('anchor', call(e['makeAnchor'], e['title']))
    e.set('version', '1.2')
    e.set('sum_class', call(e['getSummaryClass'], e['saveInfo'], e['version']))
    e.set('det_class', call(e['getDetailsClass'], e['saveInfo'], e['version']))
    e.set('output', '')
    e.set('playerOutput', '')
    e.set('meta', Obj({'hasDetails': False, 'anchor': e['anchor'], 'sum_class': e['sum_class'], 'det_class': e['det_class']}))
    e.set('separateWallets', binary('===', call(get(call(get(call(e['$'], e['xmlDoc']), 'find'), 'SaveGame > player > useSeparateWallets'), 'text')), 'true'))
    e.set('money', call(e['Number'], call(get(call(get(call(e['$'], e['xmlDoc']), 'find'), 'SaveGame > player > totalMoneyEarned'), 'text'))))
    e.set('left', e['money'])
    e.set('table', Array([]))
    e.set('output', binary('+', e['output'], binary('+', binary('+', binary('+', binary('+', '<div class="', get(e['meta'], 'anchor')), '_summary '), get(e['meta'], 'sum_class')), '">')))
    e.set('output', binary('+', e['output'], binary('+', binary('+', binary('+', binary('+', '<span class="result">', call(get(call(get(call(e['$'], e['xmlDoc']), 'find'), 'SaveGame > player > farmName'), 'html'))), ' Farm has earned '), call(e['addCommas'], e['money'])), 'g.</span><br />\n')))
    e.set('output', binary('+', e['output'], '<ul class="ach_list"><li>'))
    e.set('output', binary('+', e['output'], (call(e['getAchieveString'], 'Greenhorn', 'earn 15,000g', 1) if truth(binary('>=', e['money'], 15000)) else binary('+', binary('+', call(e['getAchieveString'], 'Greenhorn', 'earn 15,000g', 0), call(e['addCommas'], binary('-', 15000, e['money']))), 'g more'))))
    e.set('output', binary('+', e['output'], '</li>\n<li>'))
    e.set('output', binary('+', e['output'], (call(e['getAchieveString'], 'Cowpoke', 'earn 50,000g', 1) if truth(binary('>=', e['money'], 50000)) else binary('+', binary('+', call(e['getAchieveString'], 'Cowpoke', 'earn 50,000g', 0), call(e['addCommas'], binary('-', 50000, e['money']))), 'g more'))))
    e.set('output', binary('+', e['output'], '</li>\n<li>'))
    e.set('output', binary('+', e['output'], (call(e['getAchieveString'], 'Homesteader', 'earn 250,000g', 1) if truth(binary('>=', e['money'], 250000)) else binary('+', binary('+', call(e['getAchieveString'], 'Homesteader', 'earn 250,000g', 0), call(e['addCommas'], binary('-', 250000, e['money']))), 'g more'))))
    e.set('output', binary('+', e['output'], '</li>\n<li>'))
    e.set('output', binary('+', e['output'], (call(e['getAchieveString'], 'Millionaire', 'earn 1,000,000g', 1) if truth(binary('>=', e['money'], 1000000)) else binary('+', binary('+', call(e['getAchieveString'], 'Millionaire', 'earn 1,000,000g', 0), call(e['addCommas'], binary('-', 1000000, e['money']))), 'g more'))))
    e.set('output', binary('+', e['output'], '</li>\n<li>'))
    e.set('output', binary('+', e['output'], (call(e['getAchieveString'], 'Legend', 'earn 10,000,000g', 1) if truth(binary('>=', e['money'], 10000000)) else binary('+', binary('+', call(e['getAchieveString'], 'Legend', 'earn 10,000,000g', 0), call(e['addCommas'], binary('-', 10000000, e['money']))), 'g more'))))
    e.set('output', binary('+', e['output'], '</li></ul></div>'))
    if truth(e['separateWallets']):
        put(e['meta'], 'hasDetails', True)
        e.set('output', binary('+', e['output'], binary('+', binary('+', binary('+', binary('+', '<div class="', get(e['meta'], 'anchor')), '_details '), get(e['meta'], 'det_class')), '">')))
        e.set('output', binary('+', e['output'], '<span class="result">Earnings Breakdown:</span><ul class="outer">'))
        call(get(call(get(e['Object'], 'keys'), get(e['saveInfo'], 'players')), 'forEach'), Fn(callback_49, e))
        if truth(binary('>', e['left'], 0)):
            e.set('output', binary('+', e['output'], binary('+', binary('+', '<li>(', call(e['addCommas'], e['left'])), 'g surplus unexplained)</li>')))
        else:
            if truth(binary('<', e['left'], 0)):
                e.set('output', binary('+', e['output'], binary('+', binary('+', '<li>(', call(e['addCommas'], binary('-', 0, e['left']))), 'g deficit unexplained)</li>')))
        e.set('output', binary('+', e['output'], '</ul></div>'))
    e.set('output', binary('+', binary('+', call(e['getSectionHeader'], e['saveInfo'], e['title'], e['anchor'], get(e['meta'], 'hasDetails'), e['version']), e['output']), call(e['getSectionFooter'])))
    return e['output']
    return U


def callback_53(parent, this, args):
    # Upstream checkup: 1243
    e = Env(parent)
    e.declare(['type', 'who'])
    e.local['arguments'] = Array(args)
    e.set('type', call(get(call(e['$'], this), 'attr'), binary('+', get(e['saveInfo'], 'ns_prefix'), ':type')))
    e.set('who', call(get(call(get(call(e['$'], this), 'find'), 'name'), 'html')))
    if truth((_logic54 if truth(_logic54 := call(get(get(e['meta'], 'ignore'), 'hasOwnProperty'), e['type'])) else call(get(get(e['meta'], 'ignore'), 'hasOwnProperty'), e['who']))):
        return U
    put(get(e['meta'], 'npc'), e['who'], Obj({}))
    put(get(get(e['meta'], 'npc'), e['who']), 'isDatable', binary('===', call(get(call(get(call(e['$'], this), 'find'), 'datable'), 'text')), 'true'))
    put(get(get(e['meta'], 'npc'), e['who']), 'isGirl', binary('===', call(get(call(get(call(e['$'], this), 'find'), 'gender'), 'text')), '1'))
    put(get(get(e['meta'], 'npc'), e['who']), 'isChild', binary('===', e['type'], 'Child'))
    if truth(binary('<', call(e['compareSemVer'], get(e['saveInfo'], 'version'), '1.3'), 0)):
        if truth(binary('===', call(get(call(get(call(e['$'], this), 'find'), 'divorcedFromFarmer'), 'text')), 'true')):
            put(get(get(e['meta'], 'npc'), e['who']), 'relStatus', 'Divorced')
        else:
            if truth((binary('===', e['who'], call(get(e['spouse'], 'slice'), 0, unary('-', 7))) if truth(_logic55 := binary('>', get(e['meta'], 'countdown'), 0)) else _logic55)):
                put(get(get(e['meta'], 'npc'), e['who']), 'relStatus', 'Engaged')
            else:
                if truth(binary('>', call(get(call(get(call(e['$'], this), 'find'), 'daysMarried'), 'text')), 0)):
                    put(get(get(e['meta'], 'npc'), e['who']), 'relStatus', 'Married')
                else:
                    if truth(binary('===', call(get(call(get(call(e['$'], this), 'find'), 'datingFarmer'), 'text')), 'true')):
                        put(get(get(e['meta'], 'npc'), e['who']), 'relStatus', 'Dating')
                    else:
                        put(get(get(e['meta'], 'npc'), e['who']), 'relStatus', 'Friendly')
    return U


def callback_52(parent, this, args):
    # Upstream checkup: 1242
    e = Env(parent)
    e.declare([])
    e.local['arguments'] = Array(args)
    call(get(call(get(call(e['$'], this), 'find'), 'characters > NPC'), 'each'), Fn(callback_53, e))
    return U


def parseSocial_51(parent, this, args):
    # Upstream checkup: 1139
    e = Env(parent)
    e.declare(['anchor', 'det_class', 'meta', 'output', 'playerOutput', 'spouse', 'sum_class', 'table', 'title', 'version'])
    e.local['arguments'] = Array(args)
    e.local['xmlDoc'] = (args[0] if len(args) > 0 and args[0] is not U else U)
    e.local['saveInfo'] = (args[1] if len(args) > 1 and args[1] is not U else U)
    e.set('title', 'Social')
    e.set('anchor', call(e['makeAnchor'], e['title']))
    e.set('version', '1.2')
    e.set('sum_class', call(e['getSummaryClass'], e['saveInfo'], e['version']))
    e.set('det_class', call(e['getDetailsClass'], e['saveInfo'], e['version']))
    e.set('output', '')
    e.set('playerOutput', '')
    e.set('meta', Obj({'hasDetails': False, 'anchor': e['anchor'], 'sum_class': e['sum_class'], 'det_class': e['det_class']}))
    e.set('table', Array([]))
    e.set('spouse', call(get(call(get(call(e['$'], e['xmlDoc']), 'find'), 'player > spouse'), 'text')))
    put(e['meta'], 'countdown', call(e['Number'], call(get(call(get(call(e['$'], e['xmlDoc']), 'find'), 'countdownToWedding'), 'text'))))
    put(e['meta'], 'ignore', table(2))
    put(e['meta'], 'npc', Obj({}))
    put(e['meta'], 'eventList', table(3))
    if truth(binary('>=', call(e['compareSemVer'], get(e['saveInfo'], 'version'), '1.3'), 0)):
        call(get(get(get(e['meta'], 'eventList'), 'Jas'), 'push'), Array([8, 3910979]))
        call(get(get(get(e['meta'], 'eventList'), 'Vincent'), 'push'), Array([8, 3910979]))
        call(get(get(get(e['meta'], 'eventList'), 'Linus'), 'push'), Array([8, 371652]))
        call(get(get(get(e['meta'], 'eventList'), 'Pam'), 'push'), Array([9, 503180]))
        call(get(get(get(e['meta'], 'eventList'), 'Willy'), 'push'), Array([6, 711130]))
    if truth(binary('>=', call(e['compareSemVer'], get(e['saveInfo'], 'version'), '1.4'), 0)):
        call(get(get(get(e['meta'], 'eventList'), 'Gus'), 'push'), Array([5, 980558]))
        call(get(get(get(e['meta'], 'eventList'), 'Caroline'), 'push'), Array([2, 719926]))
        call(get(get(get(e['meta'], 'eventList'), 'Abigail'), 'push'), Array([14, 6963327]))
        call(get(get(get(e['meta'], 'eventList'), 'Emily'), 'push'), Array([14.1, 3917600]), Array([14.2, 3917601]))
        call(get(get(get(e['meta'], 'eventList'), 'Haley'), 'push'), Array([14.1, 6184643]), Array([14.2, 8675611]), Array([14.3, 6184644]))
        call(get(get(get(e['meta'], 'eventList'), 'Leah'), 'push'), Array([14.1, 3911124]), Array([14.2, 3091462]))
        call(get(get(get(e['meta'], 'eventList'), 'Maru'), 'push'), Array([14.1, 3917666]), Array([14.2, 5183338]))
        call(get(get(get(e['meta'], 'eventList'), 'Penny'), 'push'), Array([14.1, 4325434]), Array([14.2, 4324303]))
        call(get(get(get(e['meta'], 'eventList'), 'Alex'), 'push'), Array([14.1, 3917587]), Array([14.2, 3917589]), Array([14.3, 3917590]))
        call(get(get(get(e['meta'], 'eventList'), 'Elliott'), 'push'), Array([14.1, 3912125]), Array([14.2, 3912132]))
        call(get(get(get(e['meta'], 'eventList'), 'Harvey'), 'push'), Array([14, 3917626]))
        call(get(get(get(e['meta'], 'eventList'), 'Sam'), 'push'), Array([14.1, 3918600]), Array([14.2, 3918601]), Array([14.3, 3918602]), Array([14.4, 3918603]))
        call(get(get(get(e['meta'], 'eventList'), 'Sebastian'), 'push'), Array([14.1, 9333219]), Array([14.2, 9333220]))
        call(get(get(get(e['meta'], 'eventList'), 'Shane'), 'push'), Array([14.1, 3917584]), Array([14.2, 3917585]), Array([14.3, 3917586]))
        call(get(get(get(e['meta'], 'eventList'), 'Krobus'), 'push'), Array([14, 7771191]))
    if truth(binary('>=', call(e['compareSemVer'], get(e['saveInfo'], 'version'), '1.5'), 0)):
        put(get(e['meta'], 'eventList'), 'Leo', Array([Array([0, 1039573]), Array([2, 6497423]), Array([4, 6497421]), Array([6, 6497428]), Array([9, 8959199])]))
    call(get(call(get(call(e['$'], e['xmlDoc']), 'find'), 'locations > GameLocation'), 'each'), Fn(callback_52, e))
    put(e['table'], 0, call(e['parsePlayerSocial'], call(get(call(e['$'], e['xmlDoc']), 'find'), 'SaveGame > player'), e['saveInfo'], e['meta']))
    call(e['parseFarmhands'], e['xmlDoc'], e['saveInfo'], e['table'], e['parsePlayerSocial'], e['meta'])
    e.set('playerOutput', call(e['printTranspose'], e['table']))
    e.set('output', binary('+', binary('+', call(e['getSectionHeader'], e['saveInfo'], e['title'], e['anchor'], get(e['meta'], 'hasDetails'), e['version']), e['playerOutput']), call(e['getSectionFooter'])))
    return e['output']
    return U


def callback_57(parent, this, args):
    # Upstream checkup: 1305
    e = Env(parent)
    e.declare(['num', 'which'])
    e.local['arguments'] = Array(args)
    e.set('which', call(get(call(get(call(e['$'], this), 'find'), 'key > string'), 'text')))
    e.set('num', call(e['Number'], call(get(call(get(call(e['$'], this), 'find'), 'value > int'), 'text'))))
    if truth(binary('===', e['which'], 'dumped_Girls')):
        e.set('dumped_Girls', e['num'])
    else:
        if truth(binary('===', e['which'], 'dumped_Guys')):
            e.set('dumped_Guys', e['num'])
    return U


def callback_58(parent, this, args):
    # Upstream checkup: 1314
    e = Env(parent)
    e.declare(['isRoommate', 'num', 'who'])
    e.local['arguments'] = Array(args)
    e.set('who', call(get(call(get(call(e['$'], this), 'find'), 'key > string'), 'html')))
    if truth((_logic59 if truth(_logic59 := call(get(get(e['meta'], 'ignore'), 'hasOwnProperty'), e['who'])) else unary('!', call(get(get(e['meta'], 'npc'), 'hasOwnProperty'), e['who'])))):
        return U
    e.set('num', call(e['Number'], call(get(call(get(call(e['$'], this), 'find'), 'value > Friendship > Points'), 'text'))))
    if truth(binary('>=', e['num'], 2500)):
        update_env(e, 'count_10h', 1, False)
    if truth(binary('>=', e['num'], 1250)):
        update_env(e, 'count_5h', 1, False)
    if truth(call(get(get(e['meta'], 'eventList'), 'hasOwnProperty'), e['who'])):
        update_env(e, 'maxed_total', 1, False)
        if truth((_logic60 if truth(_logic60 := (binary('>=', e['num'], 2000) if truth(_logic61 := get(get(get(e['meta'], 'npc'), e['who']), 'isDatable')) else _logic61)) else binary('>=', e['num'], 2500))):
            update_env(e, 'maxed_count', 1, False)
    put(e['points'], e['who'], e['num'])
    put(get(get(e['meta'], 'npc'), e['who']), 'relStatus', call(get(call(get(call(e['$'], this), 'find'), 'value > Friendship > Status'), 'text')))
    e.set('isRoommate', binary('===', call(get(call(get(call(e['$'], this), 'find'), 'value > Friendship > RoommateMarriage'), 'text')), 'true'))
    if truth((e['isRoommate'] if truth(_logic62 := binary('===', get(get(get(e['meta'], 'npc'), e['who']), 'relStatus'), 'Married')) else _logic62)):
        put(get(get(e['meta'], 'npc'), e['who']), 'relStatus', 'Roommate')
    return U


def callback_63(parent, this, args):
    # Upstream checkup: 1335
    e = Env(parent)
    e.declare(['num', 'who'])
    e.local['arguments'] = Array(args)
    e.set('who', call(get(call(get(call(e['$'], this), 'find'), 'key > string'), 'html')))
    e.set('num', call(e['Number'], call(get(call(get(call(get(call(e['$'], this), 'find'), 'value > ArrayOfInt > int'), 'first')), 'text'))))
    if truth(binary('>=', e['num'], 2500)):
        update_env(e, 'count_10h', 1, False)
    if truth(binary('>=', e['num'], 1250)):
        update_env(e, 'count_5h', 1, False)
    put(e['points'], e['who'], e['num'])
    return U


def callback_65(parent, this, args):
    # Upstream checkup: 1357
    e = Env(parent)
    e.declare([])
    e.local['arguments'] = Array(args)
    e.local['e'] = (args[0] if len(args) > 0 and args[0] is not U else U)
    if truth(call(get(e['eventsSeen'], 'hasOwnProperty'), e['e'])):
        e.set('seen', True)
    return U


def callback_64(parent, this, args):
    # Upstream checkup: 1353
    e = Env(parent)
    e.declare(['extra', 'neg', 'seen'])
    e.local['arguments'] = Array(args)
    e.local['arr'] = (args[0] if len(args) > 0 and args[0] is not U else U)
    e.local['who'] = (args[1] if len(args) > 1 and args[1] is not U else U)
    e.set('seen', False)
    e.set('neg', 'no')
    call(get(call(get(call(e['String'], get(e['arr'], 1)), 'split'), '|'), 'forEach'), Fn(callback_65, e))
    if truth((_logic66 if truth(_logic66 := (_logic67 if truth(_logic67 := (_logic68 if truth(_logic68 := ((_logic70 if truth(_logic70 := call(get(e['eventsSeen'], 'hasOwnProperty'), 2123243)) else call(get(e['eventsSeen'], 'hasOwnProperty'), 2123343)) if truth(_logic69 := binary('===', get(e['arr'], 1), 101)) else _logic69)) else (binary('>', get(get(get(get(e['saveInfo'], 'data'), e['umid']), 'stats'), 'daysPlayed'), 84) if truth(_logic71 := binary('===', get(e['arr'], 1), 733330)) else _logic71))) else (binary('<', call(e['compareSemVer'], get(e['saveInfo'], 'version'), '1.5'), 0) if truth(_logic72 := (e['hasPamHouse'] if truth(_logic73 := binary('===', get(e['arr'], 1), 35)) else _logic73)) else _logic72))) else (binary('<', call(e['compareSemVer'], get(e['saveInfo'], 'version'), '1.4'), 0) if truth(_logic74 := (e['hasPamHouse'] if truth(_logic75 := binary('===', get(e['arr'], 1), 36)) else _logic75)) else _logic74))):
        e.set('neg', 'imp')
    if truth((binary('==', get(get(get(e['meta'], 'npc'), e['who']), 'relStatus'), 'Friendly') if truth(_logic76 := (get(get(get(e['meta'], 'npc'), e['who']), 'isDatable') if truth(_logic77 := binary('==', get(e['arr'], 0), 10)) else _logic77)) else _logic76)):
        e.set('neg', 'imp')
    if truth((binary('!==', e['who'], e['spouse']) if truth(_logic78 := binary('>=', get(e['arr'], 0), 14)) else _logic78)):
        e.set('neg', 'imp')
    e.set('extra', '')
    if truth(binary('===', get(e['arr'], 1), 3910979)):
        e.set('extra', ' (Jas &amp; Vincent both)')
    else:
        if truth(binary('===', get(e['arr'], 1), 639373)):
            e.set('extra', ' (Lewis &amp; Marnie both)')
    e.set('eventInfo', binary('+', e['eventInfo'], binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', ' [<span class="ms_', ('yes' if truth(e['seen']) else e['neg'])), '">'), get(e['arr'], 0)), '&#x2665;'), e['extra']), '</span>]')))
    return U


def callback_84(parent, this, args):
    # Upstream checkup: 1411
    e = Env(parent)
    e.declare([])
    e.local['arguments'] = Array(args)
    e.local['a'] = (args[0] if len(args) > 0 and args[0] is not U else U)
    e.local['b'] = (args[1] if len(args) > 1 and args[1] is not U else U)
    return binary('-', get(e['a'], 0), get(e['b'], 0))
    return U


def callback_85(parent, this, args):
    # Upstream checkup: 1412
    e = Env(parent)
    e.declare([])
    e.local['arguments'] = Array(args)
    e.local['a'] = (args[0] if len(args) > 0 and args[0] is not U else U)
    call(e['eventCheck'], e['a'], e['who'])
    return U


def callback_87(parent, this, args):
    # Upstream checkup: 1465
    e = Env(parent)
    e.declare([])
    e.local['arguments'] = Array(args)
    call(get(e['list_intro'], 'push'), call(get(call(e['$'], this), 'text')))
    e.set('hasCompletedIntroductions', False)
    return U


def parsePlayerSocial_56(parent, this, args):
    # Upstream checkup: 1276
    e = Env(parent)
    e.declare(['count_10h', 'count_5h', 'dumped_Girls', 'dumped_Guys', 'entry', 'eventCheck', 'eventInfo', 'eventsSeen', 'farmer', 'hasCompletedIntroductions', 'hasNPCSpouse', 'hasPamHouse', 'hasSpouseStardrop', 'hearts', 'id', 'list_bach', 'list_fam', 'list_intro', 'list_other', 'list_poly', 'max', 'maxed_count', 'maxed_total', 'output', 'points', 'polyamory', 'pt_pct', 'pts', 'seen', 'span', 'spouse', 'table', 'umid', 'who'])
    e.local['arguments'] = Array(args)
    e.local['player'] = (args[0] if len(args) > 0 and args[0] is not U else U)
    e.local['saveInfo'] = (args[1] if len(args) > 1 and args[1] is not U else U)
    e.local['meta'] = (args[2] if len(args) > 2 and args[2] is not U else U)
    e.set('output', '')
    e.set('table', Array([]))
    e.set('count_5h', 0)
    e.set('count_10h', 0)
    e.set('maxed_count', 0)
    e.set('maxed_total', 0)
    e.set('umid', (call(get(call(get(call(e['$'], e['player']), 'children'), 'UniqueMultiplayerID'), 'text')) if truth(binary('>=', call(e['compareSemVer'], get(e['saveInfo'], 'version'), '1.3'), 0)) else get(e['saveInfo'], 'farmerId')))
    e.set('pt_pct', '')
    e.set('points', Obj({}))
    e.set('list_fam', Array([]))
    e.set('list_bach', Array([]))
    e.set('list_other', Array([]))
    e.set('list_poly', Array([]))
    e.set('farmer', call(get(call(get(call(e['$'], e['player']), 'children'), 'name'), 'html')))
    e.set('spouse', call(get(call(get(call(e['$'], e['player']), 'children'), 'spouse'), 'html')))
    e.set('dumped_Girls', 0)
    e.set('dumped_Guys', 0)
    e.set('hasSpouseStardrop', False)
    e.set('eventsSeen', get(get(get(e['saveInfo'], 'data'), e['umid']), 'eventsSeen'))
    e.set('hasNPCSpouse', False)
    e.set('hasPamHouse', False)
    e.set('hasCompletedIntroductions', True)
    e.set('list_intro', Array([]))
    e.set('polyamory', Obj({'All Bachelors': Array([195013, 195099]), 'All Bachelorettes': Array([195012, 195019])}))
    if truth(binary('>=', call(e['compareSemVer'], get(e['saveInfo'], 'version'), '1.3'), 0)):
        call(get(call(get(call(e['$'], e['player']), 'find'), 'activeDialogueEvents > item'), 'each'), Fn(callback_57, e))
        call(get(call(get(call(e['$'], e['player']), 'find'), 'friendshipData > item'), 'each'), Fn(callback_58, e))
    else:
        call(get(call(get(call(e['$'], e['player']), 'find'), 'friendships > item'), 'each'), Fn(callback_63, e))
        if truth(binary('>', get(e['meta'], 'countdown'), 0)):
            e.set('spouse', call(get(e['spouse'], 'slice'), 0, unary('-', 7)))
    if truth(call(get(get(get(get(e['saveInfo'], 'data'), e['umid']), 'mailReceived'), 'hasOwnProperty'), 'CF_Spouse')):
        e.set('hasSpouseStardrop', True)
    if truth(call(get(get(get(get(e['saveInfo'], 'data'), e['umid']), 'mailReceived'), 'hasOwnProperty'), 'pamHouseUpgrade')):
        e.set('hasPamHouse', True)
    e.set('eventCheck', Fn(callback_64, e))
    for _key79 in keys(get(e['meta'], 'npc')):
        e.set('who', _key79)
        if truth((get(e['who'], 'isGirl') if truth(_logic80 := (get(e['who'], 'isDatable') if truth(_logic81 := binary('>', e['dumped_Girls'], 0)) else _logic81)) else _logic80)):
            put(get(get(e['meta'], 'npc'), e['who']), 'relStatus', binary('+', binary('+', 'Angry (', e['dumped_Girls']), ' more day(s))'))
        else:
            if truth((unary('!', get(e['who'], 'isGirl')) if truth(_logic82 := (get(e['who'], 'isDatable') if truth(_logic83 := binary('>', e['dumped_Guys'], 0)) else _logic83)) else _logic82)):
                put(get(get(e['nmeta'], 'npc'), e['who']), 'relStatus', binary('+', binary('+', 'Angry (', e['dumped_Guys']), ' more day(s))'))
        e.set('pts', 0)
        if truth(call(get(e['points'], 'hasOwnProperty'), e['who'])):
            e.set('pts', get(e['points'], e['who']))
        else:
            put(get(get(e['meta'], 'npc'), e['who']), 'relStatus', 'Unmet')
        e.set('hearts', call(get(e['Math'], 'floor'), binary('/', e['pts'], 250)))
        e.set('entry', '<li>')
        e.set('entry', binary('+', e['entry'], (binary('+', binary('+', binary('+', e['who'], ' ('), call(e['wikify'], 'Child', 'Children')), ')') if truth(get(get(get(e['meta'], 'npc'), e['who']), 'isChild')) else call(e['wikify'], e['who']))))
        e.set('entry', binary('+', e['entry'], binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', ': ', get(get(get(e['meta'], 'npc'), e['who']), 'relStatus')), ', '), e['hearts']), '&#x2665; ('), e['pts']), ' pts) -- ')))
        e.set('eventInfo', '')
        if truth(call(get(get(e['meta'], 'eventList'), 'hasOwnProperty'), e['who'])):
            if truth(binary('>', get(get(get(e['meta'], 'eventList'), e['who']), 'length'), 0)):
                e.set('eventInfo', binary('+', e['eventInfo'], '<ul class="compact"><li>Event(s): '))
                call(get(get(get(e['meta'], 'eventList'), e['who']), 'sort'), Fn(callback_84, e))
                call(get(get(get(e['meta'], 'eventList'), e['who']), 'forEach'), Fn(callback_85, e))
                e.set('eventInfo', binary('+', e['eventInfo'], '</li></ul>'))
        if truth(binary('===', e['who'], e['spouse'])):
            e.set('max', (3250 if truth(e['hasSpouseStardrop']) else 3375))
            if truth(binary('>=', call(e['compareSemVer'], get(e['saveInfo'], 'version'), '1.4'), 0)):
                e.set('max', 3500)
            e.set('entry', binary('+', e['entry'], ('<span class="ms_yes">MAX (can still decay)</span></li>' if truth(binary('>=', e['pts'], e['max'])) else binary('+', binary('+', '<span class="ms_no">need ', binary('-', e['max'], e['pts'])), ' more</span></li>'))))
            e.set('hasNPCSpouse', True)
            call(get(e['list_fam'], 'push'), binary('+', e['entry'], e['eventInfo']))
        else:
            if truth(get(get(get(e['meta'], 'npc'), e['who']), 'isDatable')):
                e.set('max', 2000)
                if truth(binary('===', get(get(get(e['meta'], 'npc'), e['who']), 'relStatus'), 'Dating')):
                    e.set('max', 2500)
                e.set('entry', binary('+', e['entry'], ('<span class="ms_yes">MAX</span></li>' if truth(binary('>=', e['pts'], e['max'])) else binary('+', binary('+', '<span class="ms_no">need ', binary('-', e['max'], e['pts'])), ' more</span></li>'))))
                call(get(e['list_bach'], 'push'), binary('+', e['entry'], e['eventInfo']))
            else:
                e.set('entry', binary('+', e['entry'], ('<span class="ms_yes">MAX</span></li>' if truth(binary('>=', e['pts'], 2500)) else binary('+', binary('+', '<span class="ms_no">need ', binary('-', 2500, e['pts'])), ' more</span></li>'))))
                if truth(get(get(get(e['meta'], 'npc'), e['who']), 'isChild')):
                    call(get(e['list_fam'], 'push'), binary('+', e['entry'], e['eventInfo']))
                else:
                    call(get(e['list_other'], 'push'), binary('+', e['entry'], e['eventInfo']))
    if truth(binary('>=', get(e['saveInfo'], 'version'), 1.3)):
        for _key86 in keys(e['polyamory']):
            e.set('who', _key86)
            e.set('seen', False)
            e.set('span', 'no')
            e.set('entry', binary('+', '<li>', e['who']))
            e.set('id', 0)
            while truth(binary('<', e['id'], get(get(e['polyamory'], e['who']), 'length'))):
                if truth(call(get(e['eventsSeen'], 'hasOwnProperty'), get(get(e['polyamory'], e['who']), e['id']))):
                    e.set('seen', True)
                update_env(e, 'id', 1, False)
            if truth(e['seen']):
                e.set('span', 'yes')
            else:
                if truth(e['hasNPCSpouse']):
                    e.set('span', 'imp')
            e.set('entry', binary('+', e['entry'], binary('+', binary('+', ': [<span class="ms_', e['span']), '">10&#x2665;</span>]</li>')))
            call(get(e['list_poly'], 'push'), e['entry'])
    call(get(call(get(call(e['$'], e['player']), 'find'), binary('+', binary('+', 'questLog > [', get(e['saveInfo'], 'ns_prefix')), "\\:type='SocializeQuest'] > whoToGreet > string")), 'each'), Fn(callback_87, e))
    e.set('output', binary('+', binary('+', binary('+', binary('+', '<div class="', get(e['meta'], 'anchor')), '_summary '), get(e['meta'], 'sum_class')), '">'))
    e.set('output', binary('+', e['output'], binary('+', binary('+', binary('+', binary('+', '<span class="result">', e['farmer']), ' has '), ('' if truth(e['hasCompletedIntroductions']) else 'not ')), 'met everyone in town.</span><ul class="ach_list">\n')))
    e.set('output', binary('+', e['output'], '<li>'))
    e.set('output', binary('+', e['output'], (call(e['getMilestoneString'], 'Complete <span class="ach">Introductions</span> quest', 1) if truth(binary('==', get(e['list_intro'], 'length'), 0)) else binary('+', binary('+', call(e['getMilestoneString'], 'Complete <span class="ach">Introductions</span> quest', 0), get(e['list_intro'], 'length')), ' more'))))
    e.set('output', binary('+', e['output'], '</li></ul></div>'))
    e.set('output', binary('+', e['output'], binary('+', binary('+', binary('+', binary('+', '<div class="', get(e['meta'], 'anchor')), '_details '), get(e['meta'], 'det_class')), '">')))
    if truth(binary('>', get(e['list_intro'], 'length'), 0)):
        e.set('output', binary('+', e['output'], binary('+', binary('+', '<span class="need">Villagers left to meet<ol><li>', call(get(call(get(e['list_intro'], 'sort')), 'join'), '</li><li>')), '</li></ol></span>\n')))
    e.set('output', binary('+', e['output'], '</div>'))
    call(get(e['table'], 'push'), e['output'])
    e.set('output', binary('+', binary('+', binary('+', binary('+', '<div class="', get(e['meta'], 'anchor')), '_summary '), get(e['meta'], 'sum_class')), '">'))
    e.set('output', binary('+', e['output'], binary('+', binary('+', binary('+', binary('+', '<span class="result">', e['farmer']), ' has '), e['count_5h']), ' relationship(s) of 5+ hearts.</span><ul class="ach_list">\n')))
    e.set('output', binary('+', e['output'], '<li>'))
    e.set('output', binary('+', e['output'], (call(e['getAchieveString'], 'A New Friend', '5&#x2665; with 1 person', 1) if truth(binary('>=', e['count_5h'], 1)) else binary('+', binary('+', call(e['getAchieveString'], 'A New Friend', '5&#x2665; with 1 person', 0), binary('-', 1, e['count_5h'])), ' more'))))
    e.set('output', binary('+', e['output'], '</li>\n<li>'))
    e.set('output', binary('+', e['output'], (call(e['getAchieveString'], 'Cliques', '5&#x2665; with 4 people', 1) if truth(binary('>=', e['count_5h'], 4)) else binary('+', binary('+', call(e['getAchieveString'], 'Cliques', '5&#x2665; with 4 people', 0), binary('-', 4, e['count_5h'])), ' more\n'))))
    e.set('output', binary('+', e['output'], '</li>\n<li>'))
    e.set('output', binary('+', e['output'], (call(e['getAchieveString'], 'Networking', '5&#x2665; with 10 people', 1) if truth(binary('>=', e['count_5h'], 10)) else binary('+', binary('+', call(e['getAchieveString'], 'Networking', '5&#x2665; with 10 people', 0), binary('-', 10, e['count_5h'])), ' more'))))
    e.set('output', binary('+', e['output'], '</li>\n<li>'))
    e.set('output', binary('+', e['output'], (call(e['getAchieveString'], 'Popular', '5&#x2665; with 20 people', 1) if truth(binary('>=', e['count_5h'], 20)) else binary('+', binary('+', call(e['getAchieveString'], 'Popular', '5&#x2665; with 20 people', 0), binary('-', 20, e['count_5h'])), ' more'))))
    e.set('output', binary('+', e['output'], '</li></ul></div>'))
    call(get(e['table'], 'push'), e['output'])
    e.set('output', binary('+', binary('+', binary('+', binary('+', '<div class="', get(e['meta'], 'anchor')), '_summary '), get(e['meta'], 'sum_class')), '">'))
    e.set('output', binary('+', e['output'], binary('+', binary('+', binary('+', binary('+', '<span class="result">', e['farmer']), ' has '), e['count_10h']), ' relationships of 10+ hearts.</span><ul class="ach_list">\n')))
    e.set('output', binary('+', e['output'], '<li>'))
    e.set('output', binary('+', e['output'], (call(e['getAchieveString'], 'Best Friends', '10&#x2665; with 1 person', 1) if truth(binary('>=', e['count_10h'], 1)) else binary('+', binary('+', call(e['getAchieveString'], 'Best Friends', '10&#x2665; with 1 person', 0), binary('-', 1, e['count_10h'])), ' more'))))
    e.set('output', binary('+', e['output'], '</li>\n<li>'))
    e.set('output', binary('+', e['output'], (call(e['getAchieveString'], 'The Beloved Farmer', '10&#x2665; with 8 people', 1) if truth(binary('>=', e['count_10h'], 8)) else binary('+', binary('+', call(e['getAchieveString'], 'The Beloved Farmer', '10&#x2665; with 8 people', 0), binary('-', 8, e['count_10h'])), ' more'))))
    e.set('output', binary('+', e['output'], '</li></ul></div>'))
    call(get(e['table'], 'push'), e['output'])
    if truth(binary('>=', call(e['compareSemVer'], get(e['saveInfo'], 'version'), '1.5'), 0)):
        put(get(get(e['saveInfo'], 'perfectionTracker'), e['umid']), 'Great Friends', Obj({'count': e['maxed_count'], 'total': e['maxed_total']}))
        e.set('pt_pct', call(e['getPTLink'], binary('/', e['maxed_count'], e['maxed_total']), True))
    e.set('output', binary('+', binary('+', binary('+', binary('+', '<div class="', get(e['meta'], 'anchor')), '_summary '), get(e['meta'], 'sum_class')), '">'))
    e.set('output', binary('+', e['output'], binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', '<span class="result">', e['farmer']), ' has maxed '), e['maxed_count']), ' of '), e['maxed_total']), ' base game villager relationships.'), e['pt_pct']), '</span><br />')))
    e.set('output', binary('+', e['output'], '<span class="explain">Note: for this milestone, all dateable NPCs are considered maxed at 8 hearts.</span><ul class="ach_list">\n'))
    e.set('output', binary('+', e['output'], '<li>'))
    e.set('output', binary('+', e['output'], (call(e['getMilestoneString'], 'Max out hearts with all base game villagers', 1) if truth(binary('>=', e['maxed_count'], e['maxed_total'])) else binary('+', binary('+', call(e['getMilestoneString'], 'Max out hearts with all base game villagers', 0), binary('-', e['maxed_total'], e['maxed_count'])), ' more'))))
    e.set('output', binary('+', e['output'], '</li></ul></div>'))
    call(get(e['table'], 'push'), e['output'])
    e.set('output', binary('+', binary('+', binary('+', binary('+', '<div class="', get(e['meta'], 'anchor')), '_details '), get(e['meta'], 'det_class')), '">'))
    e.set('output', binary('+', e['output'], binary('+', binary('+', '<span class="result">Individual Friendship Progress for ', e['farmer']), '</span><ul class="outer">')))
    if truth(binary('>', get(e['list_fam'], 'length'), 0)):
        e.set('output', binary('+', e['output'], binary('+', binary('+', '<li>Family (includes all player children)<ol class="compact">', call(get(call(get(e['list_fam'], 'sort')), 'join'), '')), '</ol></li>\n')))
    if truth(binary('>', get(e['list_bach'], 'length'), 0)):
        e.set('output', binary('+', e['output'], binary('+', binary('+', '<li>Datable Villagers<ol class="compact">', call(get(call(get(e['list_bach'], 'sort')), 'join'), '')), '</ol></li>\n')))
    if truth(binary('>', get(e['list_poly'], 'length'), 0)):
        e.set('output', binary('+', e['output'], binary('+', binary('+', '<li>Polyamory Events<ol class="compact">', call(get(call(get(e['list_poly'], 'sort')), 'join'), '')), '</ol></li>\n')))
    if truth(binary('>', get(e['list_other'], 'length'), 0)):
        e.set('output', binary('+', e['output'], binary('+', binary('+', '<li>Other Villagers<ol class="compact">', call(get(call(get(e['list_other'], 'sort')), 'join'), '')), '</ol></li>\n')))
    e.set('output', binary('+', e['output'], '</ul></div>'))
    put(e['meta'], 'hasDetails', True)
    call(get(e['table'], 'push'), e['output'])
    return e['table']
    return U


def parseFamily_88(parent, this, args):
    # Upstream checkup: 1546
    e = Env(parent)
    e.declare(['anchor', 'det_class', 'meta', 'output', 'playerOutput', 'sum_class', 'table', 'title', 'version'])
    e.local['arguments'] = Array(args)
    e.local['xmlDoc'] = (args[0] if len(args) > 0 and args[0] is not U else U)
    e.local['saveInfo'] = (args[1] if len(args) > 1 and args[1] is not U else U)
    e.set('title', 'Home and Family')
    e.set('anchor', call(e['makeAnchor'], e['title']))
    e.set('version', '1.2')
    e.set('sum_class', call(e['getSummaryClass'], e['saveInfo'], e['version']))
    e.set('det_class', call(e['getDetailsClass'], e['saveInfo'], e['version']))
    e.set('output', '')
    e.set('playerOutput', '')
    e.set('meta', Obj({'hasDetails': False, 'anchor': e['anchor'], 'sum_class': e['sum_class'], 'det_class': e['det_class']}))
    e.set('table', Array([]))
    put(e['meta'], 'wedding', call(e['Number'], call(get(call(get(call(e['$'], e['xmlDoc']), 'find'), 'countdownToWedding'), 'text'))))
    put(e['meta'], 'isHost', True)
    put(e['table'], 0, call(e['parsePlayerFamily'], call(get(call(e['$'], e['xmlDoc']), 'find'), 'SaveGame > player'), e['saveInfo'], e['meta']))
    call(e['parseFarmhands'], e['xmlDoc'], e['saveInfo'], e['table'], e['parsePlayerFamily'], e['meta'])
    e.set('playerOutput', binary('+', e['playerOutput'], call(e['printTranspose'], e['table'])))
    e.set('output', binary('+', binary('+', call(e['getSectionHeader'], e['saveInfo'], e['title'], e['anchor'], get(e['meta'], 'hasDetails'), e['version']), e['playerOutput']), call(e['getSectionFooter'])))
    return e['output']
    return U


def callback_95(parent, this, args):
    # Upstream checkup: 1608
    e = Env(parent)
    e.declare([])
    e.local['arguments'] = Array(args)
    update_env(e, 'count', 1, False)
    call(get(e['child_name'], 'push'), call(get(call(get(call(e['$'], this), 'find'), 'name'), 'html')))
    return U


def parsePlayerFamily_89(parent, this, args):
    # Upstream checkup: 1567
    e = Env(parent)
    e.declare(['child_name', 'children', 'count', 'farmer', 'houseType', 'houseUpgrades', 'maxUpgrades', 'needs', 'output', 'spouse', 'table', 'title', 'umid'])
    e.local['arguments'] = Array(args)
    e.local['player'] = (args[0] if len(args) > 0 and args[0] is not U else U)
    e.local['saveInfo'] = (args[1] if len(args) > 1 and args[1] is not U else U)
    e.local['meta'] = (args[2] if len(args) > 2 and args[2] is not U else U)
    e.set('output', '')
    e.set('table', Array([]))
    e.set('needs', Array([]))
    e.set('count', 0)
    e.set('maxUpgrades', (3 if truth(get(e['meta'], 'isHost')) else 2))
    e.set('houseType', ('FarmHouse' if truth(get(e['meta'], 'isHost')) else 'Cabin'))
    e.set('farmer', call(get(call(get(call(e['$'], e['player']), 'children'), 'name'), 'html')))
    e.set('spouse', call(get(call(get(call(e['$'], e['player']), 'children'), 'spouse'), 'html')))
    e.set('umid', (call(get(call(get(call(e['$'], e['player']), 'children'), 'UniqueMultiplayerID'), 'text')) if truth(binary('>=', call(e['compareSemVer'], get(e['saveInfo'], 'version'), '1.3'), 0)) else get(e['saveInfo'], 'farmerId')))
    e.set('children', '(None)')
    e.set('child_name', Array([]))
    e.set('houseUpgrades', call(e['Number'], call(get(call(get(call(e['$'], e['player']), 'children'), 'houseUpgradeLevel'), 'text'))))
    if truth((binary('>', get(e['spouse'], 'length'), 0) if truth(_logic90 := binary('!==', unary('typeof', e['spouse']), 'undefined')) else _logic90)):
        if truth((binary('<', call(e['compareSemVer'], get(e['saveInfo'], 'version'), '1.3'), 0) if truth(_logic91 := binary('>', get(e['meta'], 'wedding'), 0)) else _logic91)):
            e.set('spouse', call(get(e['spouse'], 'slice'), 0, unary('-', 7)))
        update_env(e, 'count', 1, False)
    else:
        if truth(call(get(get(e['saveInfo'], 'partners'), 'hasOwnProperty'), e['umid'])):
            e.set('spouse', get(get(e['saveInfo'], 'players'), get(get(e['saveInfo'], 'partners'), e['umid'])))
            update_env(e, 'count', 1, False)
        else:
            e.set('spouse', '(None)')
            call(get(e['needs'], 'push'), 'spouse')
    e.set('title', 'spouse')
    if truth(binary('===', e['spouse'], 'Krobus')):
        e.set('title', 'roommate')
    e.set('output', binary('+', e['output'], binary('+', binary('+', binary('+', binary('+', '<div class="', get(e['meta'], 'anchor')), '_summary '), get(e['meta'], 'sum_class')), '">')))
    e.set('output', binary('+', e['output'], binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', '<span class="result">', e['farmer']), "'s "), e['title']), ': '), e['spouse']), (binary('+', binary('+', ' -- wedding in ', get(e['meta'], 'wedding')), ' day(s)') if truth(get(e['meta'], 'wedding')) else '')), '</span><br />\n')))
    if truth((binary('>', get(get(get(e['saveInfo'], 'children'), e['umid']), 'length'), 0) if truth(_logic92 := call(get(get(e['saveInfo'], 'children'), 'hasOwnProperty'), e['umid'])) else _logic92)):
        e.set('child_name', get(get(e['saveInfo'], 'children'), e['umid']))
        e.set('count', binary('+', e['count'], get(e['child_name'], 'length')))
    else:
        if truth((binary('>', get(get(get(e['saveInfo'], 'children'), get(get(e['saveInfo'], 'partners'), e['umid'])), 'length'), 0) if truth(_logic93 := (call(get(get(e['saveInfo'], 'children'), 'hasOwnProperty'), get(get(e['saveInfo'], 'partners'), e['umid'])) if truth(_logic94 := call(get(get(e['saveInfo'], 'partners'), 'hasOwnProperty'), e['umid'])) else _logic94)) else _logic93)):
            e.set('child_name', get(get(e['saveInfo'], 'children'), get(get(e['saveInfo'], 'partners'), e['umid'])))
            e.set('count', binary('+', e['count'], get(e['child_name'], 'length')))
        else:
            call(get(call(get(call(get(call(e['$'], e['player']), 'parent')), 'find'), binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', '[', get(e['saveInfo'], 'ns_prefix')), "\\:type='"), e['houseType']), "'] NPC["), get(e['saveInfo'], 'ns_prefix')), "\\:type='Child']")), 'each'), Fn(callback_95, e))
    if truth(get(e['child_name'], 'length')):
        e.set('children', call(get(e['child_name'], 'join'), ', '))
        if truth(binary('===', get(e['child_name'], 'length'), 1)):
            call(get(e['needs'], 'push'), '1 child')
    else:
        call(get(e['needs'], 'push'), '2 children')
    e.set('output', binary('+', e['output'], binary('+', binary('+', binary('+', binary('+', '<span class="result">', e['farmer']), "'s children: "), e['children']), '</span><ul class="ach_list"><li>\n')))
    e.set('output', binary('+', e['output'], (call(e['getAchieveString'], 'Full House', 'Married + 2 kids', 1) if truth(binary('>=', e['count'], 3)) else binary('+', call(e['getAchieveString'], 'Full House', 'Married + 2 kids', 0), call(get(e['needs'], 'join'), ' and ')))))
    e.set('output', binary('+', e['output'], '</li></ul></div>'))
    call(get(e['table'], 'push'), e['output'])
    e.set('output', binary('+', binary('+', binary('+', binary('+', '<div class="', get(e['meta'], 'anchor')), '_summary '), get(e['meta'], 'sum_class')), '">'))
    e.set('output', binary('+', e['output'], binary('+', binary('+', binary('+', binary('+', '<span class="result">', e['houseType']), ' upgraded '), e['houseUpgrades']), ' time(s) of ')))
    e.set('output', binary('+', e['output'], binary('+', e['maxUpgrades'], ' possible.</span><br /><ul class="ach_list">\n')))
    e.set('output', binary('+', e['output'], '<li>'))
    e.set('output', binary('+', e['output'], (call(e['getAchieveString'], 'Moving Up', '1 upgrade', 1) if truth(binary('>=', e['houseUpgrades'], 1)) else binary('+', binary('+', call(e['getAchieveString'], 'Moving Up', '1 upgrade', 0), binary('-', 1, e['houseUpgrades'])), ' more'))))
    e.set('output', binary('+', e['output'], '</li>\n<li>'))
    e.set('output', binary('+', e['output'], (call(e['getAchieveString'], 'Living Large', '2 upgrades', 1) if truth(binary('>=', e['houseUpgrades'], 2)) else binary('+', binary('+', call(e['getAchieveString'], 'Living Large', '2 upgrades', 0), binary('-', 2, e['houseUpgrades'])), ' more'))))
    e.set('output', binary('+', e['output'], '</li>\n<li>'))
    e.set('output', binary('+', e['output'], (call(e['getMilestoneString'], 'House fully upgraded', 1) if truth(binary('>=', e['houseUpgrades'], e['maxUpgrades'])) else binary('+', binary('+', call(e['getMilestoneString'], 'House fully upgraded', 0), binary('-', e['maxUpgrades'], e['houseUpgrades'])), ' more'))))
    e.set('output', binary('+', e['output'], '</li></ul></div>'))
    call(get(e['table'], 'push'), e['output'])
    return e['table']
    return U


def parseCooking_96(parent, this, args):
    # Upstream checkup: 1643
    e = Env(parent)
    e.declare(['anchor', 'det_class', 'id', 'meta', 'output', 'playerOutput', 'sum_class', 'table', 'title', 'version'])
    e.local['arguments'] = Array(args)
    e.local['xmlDoc'] = (args[0] if len(args) > 0 and args[0] is not U else U)
    e.local['saveInfo'] = (args[1] if len(args) > 1 and args[1] is not U else U)
    e.set('title', 'Cooking')
    e.set('anchor', call(e['makeAnchor'], e['title']))
    e.set('version', '1.2')
    e.set('sum_class', call(e['getSummaryClass'], e['saveInfo'], e['version']))
    e.set('det_class', call(e['getDetailsClass'], e['saveInfo'], e['version']))
    e.set('output', '')
    e.set('playerOutput', '')
    e.set('meta', Obj({'hasDetails': False, 'anchor': e['anchor'], 'sum_class': e['sum_class'], 'det_class': e['det_class']}))
    e.set('table', Array([]))
    put(e['meta'], 'recipes', table(4))
    put(e['meta'], 'recipeTranslate', table(5))
    put(e['meta'], 'recipeReverse', Obj({}))
    if truth(binary('>=', call(e['compareSemVer'], get(e['saveInfo'], 'version'), '1.4'), 0)):
        put(get(e['meta'], 'recipes'), 733, 'Shrimp Cocktail')
        put(get(e['meta'], 'recipes'), 253, 'Triple Shot Espresso')
        put(get(e['meta'], 'recipes'), 265, 'Seafoam Pudding')
    if truth(binary('>=', call(e['compareSemVer'], get(e['saveInfo'], 'version'), '1.5'), 0)):
        put(get(e['meta'], 'recipes'), 903, 'Ginger Ale')
        put(get(e['meta'], 'recipes'), 904, 'Banana Pudding')
        put(get(e['meta'], 'recipes'), 905, 'Mango Sticky Rice')
        put(get(e['meta'], 'recipes'), 906, 'Poi')
        put(get(e['meta'], 'recipes'), 907, 'Tropical Curry')
        put(get(e['meta'], 'recipes'), 921, 'Squid Ink Ravioli')
    if truth(binary('>=', call(e['compareSemVer'], get(e['saveInfo'], 'version'), '1.6'), 0)):
        put(get(e['meta'], 'recipes'), 'MossSoup', 'Moss Soup')
    for _key97 in keys(get(e['meta'], 'recipes')):
        e.set('id', _key97)
        if truth(call(get(get(e['meta'], 'recipes'), 'hasOwnProperty'), e['id'])):
            put(get(e['meta'], 'recipeReverse'), get(get(e['meta'], 'recipes'), e['id']), e['id'])
    put(e['table'], 0, call(e['parsePlayerCooking'], call(get(call(e['$'], e['xmlDoc']), 'find'), 'SaveGame > player'), e['saveInfo'], e['meta']))
    call(e['parseFarmhands'], e['xmlDoc'], e['saveInfo'], e['table'], e['parsePlayerCooking'], e['meta'])
    e.set('playerOutput', binary('+', e['playerOutput'], call(e['printTranspose'], e['table'])))
    e.set('output', binary('+', binary('+', call(e['getSectionHeader'], e['saveInfo'], e['title'], e['anchor'], get(e['meta'], 'hasDetails'), e['version']), e['playerOutput']), call(e['getSectionFooter'])))
    return e['output']
    return U


def callback_99(parent, this, args):
    # Upstream checkup: 1788
    e = Env(parent)
    e.declare(['id', 'num'])
    e.local['arguments'] = Array(args)
    e.set('id', call(get(call(get(call(e['$'], this), 'find'), 'key > string'), 'text')))
    e.set('num', call(e['Number'], call(get(call(get(call(e['$'], this), 'find'), 'value > int'), 'text'))))
    if truth(call(get(get(e['meta'], 'recipeTranslate'), 'hasOwnProperty'), e['id'])):
        e.set('id', get(get(e['meta'], 'recipeTranslate'), e['id']))
    if truth(call(get(get(e['meta'], 'recipeReverse'), 'hasOwnProperty'), e['id'])):
        put(e['known'], e['id'], e['num'])
        update_env(e, 'known_count', 1, False)
    else:
        call(get(e['console'], 'log'), binary('+', 'Unrecognized cooking recipe: ', e['id']))
        update_env(e, 'mod_known', 1, False)
    return U


def callback_100(parent, this, args):
    # Upstream checkup: 1802
    e = Env(parent)
    e.declare(['id', 'num'])
    e.local['arguments'] = Array(args)
    e.set('id', call(get(call(get(call(e['$'], this), 'find'), 'key > *'), 'text')))
    e.set('num', call(e['Number'], call(get(call(get(call(e['$'], this), 'find'), 'value > int'), 'text'))))
    if truth(call(get(get(e['meta'], 'recipes'), 'hasOwnProperty'), e['id'])):
        if truth(binary('>', e['num'], 0)):
            put(e['crafted'], get(get(e['meta'], 'recipes'), e['id']), e['num'])
            update_env(e, 'craft_count', 1, False)
    else:
        if truth(binary('>', e['num'], 0)):
            update_env(e, 'mod_craft', 1, False)
    return U


def parsePlayerCooking_98(parent, this, args):
    # Upstream checkup: 1770
    e = Env(parent)
    e.declare(['craft_count', 'crafted', 'id', 'known', 'known_count', 'mod_craft', 'mod_known', 'need_c', 'need_k', 'output', 'pt_pct', 'r', 'recipe_count', 'umid'])
    e.local['arguments'] = Array(args)
    e.local['player'] = (args[0] if len(args) > 0 and args[0] is not U else U)
    e.local['saveInfo'] = (args[1] if len(args) > 1 and args[1] is not U else U)
    e.local['meta'] = (args[2] if len(args) > 2 and args[2] is not U else U)
    e.set('output', '')
    e.set('recipe_count', get(call(get(e['Object'], 'keys'), get(e['meta'], 'recipes')), 'length'))
    e.set('known', Obj({}))
    e.set('known_count', 0)
    e.set('crafted', Obj({}))
    e.set('craft_count', 0)
    e.set('need_k', Array([]))
    e.set('need_c', Array([]))
    e.set('mod_known', 0)
    e.set('mod_craft', 0)
    e.set('umid', (call(get(call(get(call(e['$'], e['player']), 'children'), 'UniqueMultiplayerID'), 'text')) if truth(binary('>=', call(e['compareSemVer'], get(e['saveInfo'], 'version'), '1.3'), 0)) else get(e['saveInfo'], 'farmerId')))
    e.set('pt_pct', '')
    call(get(call(get(call(e['$'], e['player']), 'find'), 'cookingRecipes > item'), 'each'), Fn(callback_99, e))
    call(get(call(get(call(e['$'], e['player']), 'find'), 'recipesCooked > item'), 'each'), Fn(callback_100, e))
    if truth(binary('>=', call(e['compareSemVer'], get(e['saveInfo'], 'version'), '1.5'), 0)):
        put(get(get(e['saveInfo'], 'perfectionTracker'), e['umid']), 'Cooking', Obj({'count': e['craft_count'], 'total': e['recipe_count']}))
        e.set('pt_pct', call(e['getPTLink'], binary('/', e['craft_count'], e['recipe_count']), True))
    e.set('output', binary('+', e['output'], binary('+', binary('+', binary('+', binary('+', '<div class="', get(e['meta'], 'anchor')), '_summary '), get(e['meta'], 'sum_class')), '">')))
    e.set('output', binary('+', e['output'], binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', '<span class="result">', call(get(call(get(call(e['$'], e['player']), 'children'), 'name'), 'html'))), ' has cooked '), e['craft_count']), ' and knows '), e['known_count']), ' of '), e['recipe_count']), (' base game' if truth(binary('>', e['mod_known'], 0)) else '')), ' recipes.'), e['pt_pct']), '</span>\n')))
    if truth(binary('>', e['mod_known'], 0)):
        e.set('output', binary('+', e['output'], binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', '<br /><span class="result note">', call(get(call(get(call(e['$'], e['player']), 'children'), 'name'), 'html'))), ' has also cooked '), e['mod_craft']), ' and knows '), e['mod_known']), ' unrecognized (probably mod) recipes.</span>\n')))
    e.set('output', binary('+', e['output'], '<ul class="ach_list"><li>'))
    e.set('output', binary('+', e['output'], (call(e['getAchieveString'], 'Cook', 'cook 10 different recipes', 1) if truth(binary('>=', binary('+', e['craft_count'], e['mod_craft']), 10)) else binary('+', binary('+', call(e['getAchieveString'], 'Cook', 'cook 10 different recipes', 0), binary('-', binary('-', 10, e['craft_count']), e['mod_craft'])), ' more'))))
    e.set('output', binary('+', e['output'], '</li>\n<li>'))
    e.set('output', binary('+', e['output'], (call(e['getAchieveString'], 'Sous Chef', 'cook 25 different recipes', 1) if truth(binary('>=', binary('+', e['craft_count'], e['mod_craft']), 25)) else binary('+', binary('+', call(e['getAchieveString'], 'Sous Chef', 'cook 25 different recipes', 0), binary('-', binary('-', 25, e['craft_count']), e['mod_craft'])), ' more'))))
    e.set('output', binary('+', e['output'], '</li>\n<li>'))
    e.set('output', binary('+', e['output'], (call(e['getAchieveString'], 'Gourmet Chef', 'cook every recipe', 1) if truth(binary('>=', binary('+', e['craft_count'], e['mod_craft']), binary('+', e['recipe_count'], e['mod_known']))) else binary('+', binary('+', binary('+', call(e['getAchieveString'], 'Gourmet Chef', 'cook every recipe', 0), ('at least ' if truth(binary('>', e['mod_known'], 0)) else '')), binary('-', binary('-', binary('+', e['recipe_count'], e['mod_known']), e['craft_count']), e['mod_craft'])), ' more'))))
    e.set('output', binary('+', e['output'], '</li></ul></div>'))
    if truth(binary('<', binary('+', e['craft_count'], e['mod_craft']), binary('+', e['recipe_count'], e['mod_known']))):
        for _key101 in keys(get(e['meta'], 'recipes')):
            e.set('id', _key101)
            if truth(call(get(get(e['meta'], 'recipes'), 'hasOwnProperty'), e['id'])):
                e.set('r', get(get(e['meta'], 'recipes'), e['id']))
                if truth(unary('!', call(get(e['known'], 'hasOwnProperty'), e['r']))):
                    call(get(e['need_k'], 'push'), binary('+', binary('+', '<li>', call(e['wikify'], e['r'])), '</li>'))
                else:
                    if truth(unary('!', call(get(e['crafted'], 'hasOwnProperty'), e['r']))):
                        call(get(e['need_c'], 'push'), binary('+', binary('+', '<li>', call(e['wikify'], e['r'])), '</li>'))
        put(e['meta'], 'hasDetails', True)
        e.set('output', binary('+', e['output'], binary('+', binary('+', binary('+', binary('+', '<div class="', get(e['meta'], 'anchor')), '_details '), get(e['meta'], 'det_class')), '">')))
        e.set('output', binary('+', e['output'], '<span class="need">Left to cook:<ul>'))
        if truth(binary('>', get(e['need_c'], 'length'), 0)):
            e.set('output', binary('+', e['output'], binary('+', binary('+', '<li>Known Recipes<ol>', call(get(call(get(e['need_c'], 'sort')), 'join'), '')), '</ol></li>\n')))
        if truth(binary('>', get(e['need_k'], 'length'), 0)):
            e.set('output', binary('+', e['output'], binary('+', binary('+', '<li>Unknown Recipes<ol>', call(get(call(get(e['need_k'], 'sort')), 'join'), '')), '</ol></li>\n')))
        if truth(binary('>', e['mod_known'], 0)):
            if truth(binary('>=', e['mod_craft'], e['mod_known'])):
                e.set('output', binary('+', e['output'], '<li>Possibly additional mod recipes</li>'))
            else:
                e.set('output', binary('+', e['output'], binary('+', binary('+', '<li>Plus at least ', binary('-', e['mod_known'], e['mod_craft'])), ' mod recipes</li>')))
        e.set('output', binary('+', e['output'], '</ul></span></div>'))
    return Array([e['output']])
    return U


def parseCrafting_102(parent, this, args):
    # Upstream checkup: 1872
    e = Env(parent)
    e.declare(['anchor', 'det_class', 'meta', 'output', 'playerOutput', 'sum_class', 'table', 'title', 'version'])
    e.local['arguments'] = Array(args)
    e.local['xmlDoc'] = (args[0] if len(args) > 0 and args[0] is not U else U)
    e.local['saveInfo'] = (args[1] if len(args) > 1 and args[1] is not U else U)
    e.set('title', 'Crafting')
    e.set('anchor', call(e['makeAnchor'], e['title']))
    e.set('version', '1.2')
    e.set('sum_class', call(e['getSummaryClass'], e['saveInfo'], e['version']))
    e.set('det_class', call(e['getDetailsClass'], e['saveInfo'], e['version']))
    e.set('output', '')
    e.set('playerOutput', '')
    e.set('meta', Obj({'hasDetails': False, 'anchor': e['anchor'], 'sum_class': e['sum_class'], 'det_class': e['det_class']}))
    e.set('table', Array([]))
    put(e['meta'], 'recipes', table(6))
    put(e['meta'], 'recipeTranslate', Obj({'Oil Of Garlic': 'Oil of Garlic'}))
    if truth(binary('>=', call(e['compareSemVer'], get(e['saveInfo'], 'version'), '1.3'), 0)):
        call(get(get(e['meta'], 'recipes'), 'push'), 'Wood Sign', 'Stone Sign', 'Garden Pot')
    if truth(binary('>=', call(e['compareSemVer'], get(e['saveInfo'], 'version'), '1.4'), 0)):
        call(get(get(e['meta'], 'recipes'), 'push'), 'Brick Floor', 'Grass Starter', 'Deluxe Scarecrow', 'Mini-Jukebox', 'Tree Fertilizer', 'Tea Sapling', 'Warp Totem: Desert')
    if truth(binary('>=', call(e['compareSemVer'], get(e['saveInfo'], 'version'), '1.5'), 0)):
        call(get(get(e['meta'], 'recipes'), 'push'), 'Rustic Plank Floor', 'Stone Walkway Floor', 'Fairy Dust', 'Bug Steak', 'Dark Sign', 'Quality Bobber', 'Stone Chest', 'Monster Musk', 'Mini-Obelisk', 'Farm Computer', 'Ostrich Incubator', 'Geode Crusher', 'Fiber Seeds', 'Solar Panel', 'Bone Mill', 'Warp Totem: Island', 'Thorns Ring', 'Glowstone Ring', 'Heavy Tapper', 'Hopper', 'Magic Bait', 'Hyper Speed-Gro', 'Deluxe Fertilizer', 'Deluxe Retaining Soil', 'Cookout Kit')
    if truth(binary('>=', call(e['compareSemVer'], get(e['saveInfo'], 'version'), '1.6'), 0)):
        call(get(get(e['meta'], 'recipes'), 'push'), 'Anvil', 'Bait Maker', 'Big Chest', 'Big Stone Chest', 'Blue Grass Starter', 'Challenge Bait', 'Dehydrator', 'Deluxe Bait', 'Deluxe Worm Bin', 'Fish Smoker', 'Heavy Furnace', 'Mini-Forge', 'Mushroom Log', 'Mystic Tree Seed', 'Sonar Bobber', 'Statue Of Blessings', 'Statue Of The Dwarf King', 'Tent Kit', 'Text Sign', 'Treasure Totem')
    put(e['table'], 0, call(e['parsePlayerCrafting'], call(get(call(e['$'], e['xmlDoc']), 'find'), 'SaveGame > player'), e['saveInfo'], e['meta']))
    call(e['parseFarmhands'], e['xmlDoc'], e['saveInfo'], e['table'], e['parsePlayerCrafting'], e['meta'])
    e.set('playerOutput', binary('+', e['playerOutput'], call(e['printTranspose'], e['table'])))
    e.set('output', binary('+', binary('+', call(e['getSectionHeader'], e['saveInfo'], e['title'], e['anchor'], get(e['meta'], 'hasDetails'), e['version']), e['playerOutput']), call(e['getSectionFooter'])))
    return e['output']
    return U


def callback_104(parent, this, args):
    # Upstream checkup: 1947
    e = Env(parent)
    e.declare(['id', 'num'])
    e.local['arguments'] = Array(args)
    e.set('id', call(get(call(get(call(e['$'], this), 'find'), 'key > string'), 'text')))
    e.set('num', call(e['Number'], call(get(call(get(call(e['$'], this), 'find'), 'value > int'), 'text'))))
    if truth(call(get(get(e['meta'], 'recipeTranslate'), 'hasOwnProperty'), e['id'])):
        e.set('id', get(get(e['meta'], 'recipeTranslate'), e['id']))
    if truth(binary('===', e['id'], 'Wedding Ring')):
        return True
    if truth(binary('===', call(get(get(e['meta'], 'recipes'), 'indexOf'), e['id']), unary('-', 1))):
        update_env(e, 'mod_known', 1, False)
        if truth(binary('>', e['num'], 0)):
            update_env(e, 'mod_craft', 1, False)
        call(get(e['console'], 'log'), binary('+', 'Unrecognized crafting recipe: ', e['id']))
        return True
    put(e['known'], e['id'], e['num'])
    update_env(e, 'known_count', 1, False)
    if truth(binary('>', e['num'], 0)):
        update_env(e, 'craft_count', 1, False)
    else:
        call(get(e['need_c'], 'push'), binary('+', binary('+', '<li>', call(e['wikify'], e['id'])), '</li>'))
    return U


def parsePlayerCrafting_103(parent, this, args):
    # Upstream checkup: 1931
    e = Env(parent)
    e.declare(['craft_count', 'id', 'known', 'known_count', 'mod_craft', 'mod_known', 'need_c', 'need_k', 'output', 'pt_pct', 'r', 'recipe_count', 'umid'])
    e.local['arguments'] = Array(args)
    e.local['player'] = (args[0] if len(args) > 0 and args[0] is not U else U)
    e.local['saveInfo'] = (args[1] if len(args) > 1 and args[1] is not U else U)
    e.local['meta'] = (args[2] if len(args) > 2 and args[2] is not U else U)
    e.set('output', '')
    e.set('known', Obj({}))
    e.set('known_count', 0)
    e.set('craft_count', 0)
    e.set('need_k', Array([]))
    e.set('need_c', Array([]))
    e.set('mod_known', 0)
    e.set('mod_craft', 0)
    e.set('umid', (call(get(call(get(call(e['$'], e['player']), 'children'), 'UniqueMultiplayerID'), 'text')) if truth(binary('>=', call(e['compareSemVer'], get(e['saveInfo'], 'version'), '1.3'), 0)) else get(e['saveInfo'], 'farmerId')))
    e.set('pt_pct', '')
    e.set('recipe_count', get(get(e['meta'], 'recipes'), 'length'))
    call(get(call(get(call(e['$'], e['player']), 'find'), 'craftingRecipes > item'), 'each'), Fn(callback_104, e))
    if truth(binary('>=', call(e['compareSemVer'], get(e['saveInfo'], 'version'), '1.5'), 0)):
        put(get(get(e['saveInfo'], 'perfectionTracker'), e['umid']), 'Crafting', Obj({'count': e['craft_count'], 'total': e['recipe_count']}))
        e.set('pt_pct', call(e['getPTLink'], binary('/', e['craft_count'], e['recipe_count']), True))
    e.set('output', binary('+', e['output'], binary('+', binary('+', binary('+', binary('+', '<div class="', get(e['meta'], 'anchor')), '_summary '), get(e['meta'], 'sum_class')), '">')))
    e.set('output', binary('+', e['output'], binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', '<span class="result">', call(get(call(get(call(e['$'], e['player']), 'children'), 'name'), 'html'))), ' has crafted '), e['craft_count']), ' and knows '), e['known_count']), ' of '), e['recipe_count']), ' base game recipes.'), e['pt_pct']), '</span>\n')))
    if truth(binary('>', e['mod_known'], 0)):
        e.set('output', binary('+', e['output'], binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', '<br /><span class="result note">', call(get(call(get(call(e['$'], e['player']), 'children'), 'name'), 'html'))), ' has also crafted '), e['mod_craft']), ' and knows '), e['mod_known']), ' unrecognized (probably mod) recipes.</span>')))
    e.set('output', binary('+', e['output'], '<ul class="ach_list"><li>'))
    e.set('output', binary('+', e['output'], (call(e['getAchieveString'], 'D.I.Y.', 'craft 15 different items', 1) if truth(binary('>=', binary('+', e['craft_count'], e['mod_craft']), 15)) else binary('+', binary('+', call(e['getAchieveString'], 'D.I.Y.', 'craft 15 different items', 0), binary('-', binary('-', 15, e['craft_count']), e['mod_craft'])), ' more'))))
    e.set('output', binary('+', e['output'], '</li>\n<li>'))
    e.set('output', binary('+', e['output'], (call(e['getAchieveString'], 'Artisan', 'craft 30 different items', 1) if truth(binary('>=', binary('+', e['craft_count'], e['mod_craft']), 30)) else binary('+', binary('+', call(e['getAchieveString'], 'Artisan', 'craft 30 different items', 0), binary('-', binary('-', 30, e['craft_count']), e['mod_craft'])), ' more'))))
    e.set('output', binary('+', e['output'], '</li>\n<li>'))
    e.set('output', binary('+', e['output'], (call(e['getAchieveString'], 'Craft Master', 'craft every item', 1) if truth(binary('>=', binary('+', e['craft_count'], e['mod_craft']), binary('+', e['recipe_count'], e['mod_known']))) else binary('+', binary('+', binary('+', call(e['getAchieveString'], 'Craft Master', 'craft every item', 0), ('at least ' if truth(binary('>', e['mod_known'], 0)) else '')), binary('-', binary('-', binary('+', e['recipe_count'], e['mod_known']), e['craft_count']), e['mod_craft'])), ' more'))))
    e.set('output', binary('+', e['output'], '</li></ul></div>'))
    if truth(binary('<', binary('+', e['craft_count'], e['mod_craft']), binary('+', e['recipe_count'], e['mod_known']))):
        put(e['meta'], 'hasDetails', True)
        e.set('output', binary('+', e['output'], binary('+', binary('+', binary('+', binary('+', '<div class="', get(e['meta'], 'anchor')), '_details '), get(e['meta'], 'det_class')), '">')))
        e.set('output', binary('+', e['output'], '<span class="need">Left to craft:<ul>'))
        if truth(binary('>', get(e['need_c'], 'length'), 0)):
            e.set('output', binary('+', e['output'], binary('+', binary('+', '<li>Known Recipes<ol>', call(get(call(get(e['need_c'], 'sort')), 'join'), '')), '</ol></li>\n')))
        if truth(binary('<', e['known_count'], e['recipe_count'])):
            e.set('need_k', Array([]))
            for _key105 in keys(get(e['meta'], 'recipes')):
                e.set('id', _key105)
                if truth(call(get(get(e['meta'], 'recipes'), 'hasOwnProperty'), e['id'])):
                    e.set('r', get(get(e['meta'], 'recipes'), e['id']))
                    if truth(unary('!', call(get(e['known'], 'hasOwnProperty'), e['r']))):
                        call(get(e['need_k'], 'push'), binary('+', binary('+', '<li>', call(e['wikify'], e['r'])), '</li>'))
            e.set('output', binary('+', e['output'], binary('+', binary('+', '<li>Unknown Recipes<ol>', call(get(call(get(e['need_k'], 'sort')), 'join'), '')), '</ol></li>')))
        if truth(binary('>', e['mod_known'], 0)):
            if truth(binary('>=', e['mod_craft'], e['mod_known'])):
                e.set('output', binary('+', e['output'], '<li>Possibly additional mod recipes</li>'))
            else:
                e.set('output', binary('+', e['output'], binary('+', binary('+', '<li>Plus at least ', binary('-', e['mod_known'], e['mod_craft'])), ' mod recipes</li>')))
        e.set('output', binary('+', e['output'], '</ul></span></div>'))
    return Array([e['output']])
    return U


def parseFishing_106(parent, this, args):
    # Upstream checkup: 2028
    e = Env(parent)
    e.declare(['anchor', 'det_class', 'meta', 'output', 'playerOutput', 'sum_class', 'table', 'title', 'version'])
    e.local['arguments'] = Array(args)
    e.local['xmlDoc'] = (args[0] if len(args) > 0 and args[0] is not U else U)
    e.local['saveInfo'] = (args[1] if len(args) > 1 and args[1] is not U else U)
    e.set('title', 'Fishing')
    e.set('anchor', call(e['makeAnchor'], e['title']))
    e.set('version', '1.2')
    e.set('sum_class', call(e['getSummaryClass'], e['saveInfo'], e['version']))
    e.set('det_class', call(e['getDetailsClass'], e['saveInfo'], e['version']))
    e.set('output', '')
    e.set('playerOutput', '')
    e.set('meta', Obj({'hasDetails': False, 'anchor': e['anchor'], 'sum_class': e['sum_class'], 'det_class': e['det_class']}))
    e.set('table', Array([]))
    put(e['meta'], 'recipes', table(7))
    put(e['meta'], 'bobber', Obj({}))
    if truth(binary('>=', call(e['compareSemVer'], get(e['saveInfo'], 'version'), '1.3'), 0)):
        put(get(e['meta'], 'recipes'), 798, 'Midnight Squid')
        put(get(e['meta'], 'recipes'), 799, 'Spook Fish')
        put(get(e['meta'], 'recipes'), 800, 'Blobfish')
    if truth(binary('>=', call(e['compareSemVer'], get(e['saveInfo'], 'version'), '1.4'), 0)):
        put(get(e['meta'], 'recipes'), 269, 'Midnight Carp')
        put(get(e['meta'], 'recipes'), 267, 'Flounder')
    if truth(binary('>=', call(e['compareSemVer'], get(e['saveInfo'], 'version'), '1.5'), 0)):
        put(get(e['meta'], 'recipes'), 836, 'Stingray')
        put(get(e['meta'], 'recipes'), 837, 'Lionfish')
        put(get(e['meta'], 'recipes'), 838, 'Blue Discus')
    if truth(binary('>=', call(e['compareSemVer'], get(e['saveInfo'], 'version'), '1.6'), 0)):
        put(get(e['meta'], 'recipes'), 'Goby', 'Goby')
        put(get(e['meta'], 'recipes'), 'CaveJelly', 'Cave Jelly')
        put(get(e['meta'], 'recipes'), 'RiverJelly', 'River Jelly')
        put(get(e['meta'], 'recipes'), 'SeaJelly', 'Sea Jelly')
        put(get(e['meta'], 'recipes'), 372, 'Clam')
        put(get(e['meta'], 'bobber'), 898, 'Son of Crimsonfish')
        put(get(e['meta'], 'bobber'), 899, 'Ms. Angler')
        put(get(e['meta'], 'bobber'), 900, 'Legend II')
        put(get(e['meta'], 'bobber'), 901, 'Radioactive Carp')
        put(get(e['meta'], 'bobber'), 902, 'Glacierfish Jr.')
    put(e['table'], 0, call(e['parsePlayerFishing'], call(get(call(e['$'], e['xmlDoc']), 'find'), 'SaveGame > player'), e['saveInfo'], e['meta']))
    call(e['parseFarmhands'], e['xmlDoc'], e['saveInfo'], e['table'], e['parsePlayerFishing'], e['meta'])
    e.set('playerOutput', binary('+', e['playerOutput'], call(e['printTranspose'], e['table'])))
    e.set('output', binary('+', binary('+', call(e['getSectionHeader'], e['saveInfo'], e['title'], e['anchor'], get(e['meta'], 'hasDetails'), e['version']), e['playerOutput']), call(e['getSectionFooter'])))
    return e['output']
    return U


def callback_108(parent, this, args):
    # Upstream checkup: 2188
    e = Env(parent)
    e.declare(['id', 'num', 'paren', 'raw_id'])
    e.local['arguments'] = Array(args)
    e.set('raw_id', call(get(call(get(call(e['$'], this), 'find'), 'key > *'), 'text')))
    e.set('num', call(e['Number'], call(get(call(get(call(get(call(e['$'], this), 'find'), 'value > ArrayOfInt > int'), 'first')), 'text'))))
    e.set('id', e['raw_id'])
    e.set('paren', call(get(e['raw_id'], 'indexOf'), ')'))
    if truth(binary('>', e['paren'], unary('-', 1))):
        e.set('id', call(get(e['raw_id'], 'substring'), binary('+', e['paren'], 1)))
    if truth(binary('>', e['num'], 0)):
        update_env(e, 'bobber_count', 1, False)
        if truth(unary('!', call(get(e['ignore'], 'hasOwnProperty'), e['id']))):
            e.set('count', binary('+', e['count'], e['num']))
            if truth(call(get(get(e['meta'], 'recipes'), 'hasOwnProperty'), e['id'])):
                update_env(e, 'craft_count', 1, False)
                put(e['known'], get(get(e['meta'], 'recipes'), e['id']), e['num'])
            else:
                if truth(call(get(get(e['meta'], 'bobber'), 'hasOwnProperty'), e['id'])):
                    put(e['known'], get(get(e['meta'], 'bobber'), e['id']), e['num'])
                else:
                    call(get(e['console'], 'log'), binary('+', 'Unrecognized fish ID: ', e['raw_id']))
                    update_env(e, 'mod_count', 1, False)
    if truth(call(get(e['ignore'], 'hasOwnProperty'), e['id'])):
        call(get(e['console'], 'log'), binary('+', binary('+', binary('+', binary('+', binary('+', call(get(call(get(call(e['$'], e['player']), 'children'), 'name'), 'html')), ' has caught non-fish item '), e['raw_id']), ' ('), e['num']), ')'))
    return U


def parsePlayerFishing_107(parent, this, args):
    # Upstream checkup: 2137
    e = Env(parent)
    e.declare(['achieve_left', 'bobber_count', 'bobber_fish_left', 'bobbers_unlocked', 'count', 'craft_count', 'id', 'ignore', 'known', 'mod_count', 'need', 'output', 'pt_pct', 'r', 'recipe_count', 'total_bobbers', 'umid'])
    e.local['arguments'] = Array(args)
    e.local['player'] = (args[0] if len(args) > 0 and args[0] is not U else U)
    e.local['saveInfo'] = (args[1] if len(args) > 1 and args[1] is not U else U)
    e.local['meta'] = (args[2] if len(args) > 2 and args[2] is not U else U)
    e.set('output', '')
    e.set('recipe_count', get(call(get(e['Object'], 'keys'), get(e['meta'], 'recipes')), 'length'))
    e.set('count', 0)
    e.set('craft_count', 0)
    e.set('bobber_count', 0)
    e.set('mod_count', 0)
    e.set('known', Array([]))
    e.set('need', Array([]))
    e.set('ignore', table(8))
    e.set('umid', (call(get(call(get(call(e['$'], e['player']), 'children'), 'UniqueMultiplayerID'), 'text')) if truth(binary('>=', call(e['compareSemVer'], get(e['saveInfo'], 'version'), '1.3'), 0)) else get(e['saveInfo'], 'farmerId')))
    e.set('pt_pct', '')
    if truth(binary('<', call(e['compareSemVer'], get(e['saveInfo'], 'version'), '1.6'), 0)):
        put(e['ignore'], 372, 1)
        put(e['ignore'], 898, 1)
        put(e['ignore'], 899, 1)
        put(e['ignore'], 900, 1)
        put(e['ignore'], 901, 1)
        put(e['ignore'], 902, 1)
    call(get(call(get(call(e['$'], e['player']), 'find'), 'fishCaught > item'), 'each'), Fn(callback_108, e))
    if truth(binary('>=', call(e['compareSemVer'], get(e['saveInfo'], 'version'), '1.5'), 0)):
        put(get(get(e['saveInfo'], 'perfectionTracker'), e['umid']), 'Fishing', Obj({'count': e['craft_count'], 'total': e['recipe_count']}))
        e.set('pt_pct', call(e['getPTLink'], binary('/', e['craft_count'], e['recipe_count']), True))
    e.set('output', binary('+', e['output'], binary('+', binary('+', binary('+', binary('+', '<div class="', get(e['meta'], 'anchor')), '_summary '), get(e['meta'], 'sum_class')), '">')))
    e.set('output', binary('+', e['output'], binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', '<span class="result">', call(get(call(get(call(e['$'], e['player']), 'children'), 'name'), 'html'))), ' has '), e['count']), ' total catches and has caught '), e['craft_count']), ' of '), e['recipe_count']), ' base game fish.'), e['pt_pct']), '</span>')))
    if truth(binary('>', e['mod_count'], 0)):
        e.set('output', binary('+', e['output'], binary('+', binary('+', binary('+', binary('+', '<br /><span class="result note">', call(get(call(get(call(e['$'], e['player']), 'children'), 'name'), 'html'))), ' has also caught '), e['mod_count']), ' unrecognized (probably mod) fish.</span>')))
    e.set('output', binary('+', e['output'], '<ul class="ach_list"><li>'))
    e.set('output', binary('+', e['output'], (call(e['getAchieveString'], 'Mother Catch', 'catch 100 total fish', 1) if truth(binary('>=', e['count'], 100)) else binary('+', binary('+', call(e['getAchieveString'], 'Mother Catch', 'catch 100 total fish', 0), binary('-', 100, e['count'])), ' more'))))
    e.set('output', binary('+', e['output'], '</li>\n<li>'))
    e.set('output', binary('+', e['output'], (call(e['getAchieveString'], 'Fisherman', 'catch 10 different fish', 1) if truth(binary('>=', e['craft_count'], 10)) else binary('+', binary('+', call(e['getAchieveString'], 'Fisherman', 'catch 10 different fish', 0), binary('-', 10, e['craft_count'])), ' more'))))
    e.set('output', binary('+', e['output'], '</li>\n<li>'))
    e.set('output', binary('+', e['output'], (call(e['getAchieveString'], "Ol' Mariner", 'catch 24 different fish', 1) if truth(binary('>=', e['craft_count'], 24)) else binary('+', binary('+', call(e['getAchieveString'], "Ol' Mariner", 'catch 24 different fish', 0), binary('-', 24, e['craft_count'])), ' more'))))
    e.set('output', binary('+', e['output'], '</li>\n<li>'))
    if truth(binary('>=', call(e['compareSemVer'], get(e['saveInfo'], 'version'), '1.4'), 0)):
        e.set('output', binary('+', e['output'], (call(e['getAchieveString'], 'Master Angler', 'catch every type of fish', 1) if truth(binary('>=', e['craft_count'], e['recipe_count'])) else binary('+', binary('+', call(e['getAchieveString'], 'Master Angler', 'catch every type of fish', 0), binary('-', e['recipe_count'], e['craft_count'])), ' more'))))
    else:
        e.set('output', binary('+', e['output'], (call(e['getAchieveString'], 'Master Angler', 'catch 59 different fish', 1) if truth(binary('>=', e['craft_count'], call(get(e['Math'], 'min'), 59, e['recipe_count']))) else binary('+', binary('+', call(e['getAchieveString'], 'Master Angler', 'catch 59 different fish', 0), binary('-', call(get(e['Math'], 'min'), 59, e['recipe_count']), e['craft_count'])), ' more'))))
        if truth(binary('===', call(e['compareSemVer'], get(e['saveInfo'], 'version'), '1.3'), 0)):
            e.set('output', binary('+', e['output'], '</li>\n<li>'))
            e.set('output', binary('+', e['output'], (call(e['getMilestoneString'], 'Catch every type of fish', 1) if truth(binary('>=', e['craft_count'], e['recipe_count'])) else binary('+', binary('+', call(e['getMilestoneString'], 'Catch every type of fish', 0), binary('-', e['recipe_count'], e['craft_count'])), ' more'))))
    e.set('output', binary('+', e['output'], '</li></ul>'))
    e.set('total_bobbers', 39)
    e.set('bobbers_unlocked', call(get(e['Math'], 'min'), e['total_bobbers'], binary('+', 1, call(get(e['Math'], 'floor'), binary('/', e['bobber_count'], 2)))))
    e.set('bobber_fish_left', binary('-', binary('*', 2, binary('-', e['total_bobbers'], 1)), e['bobber_count']))
    if truth(binary('>=', call(e['compareSemVer'], get(e['saveInfo'], 'version'), '1.6'), 0)):
        e.set('output', binary('+', e['output'], binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', '<span class="result">', call(get(call(get(call(e['$'], e['player']), 'children'), 'name'), 'html'))), ' has unlocked '), e['bobbers_unlocked']), ' of '), e['total_bobbers']), ' bobber styles.</span>')))
        e.set('output', binary('+', e['output'], '<ul class="ach_list"><li>'))
        e.set('output', binary('+', e['output'], (call(e['getMilestoneString'], 'Unlock every bobber style', 1) if truth(binary('>=', e['bobbers_unlocked'], e['total_bobbers'])) else binary('+', binary('+', call(e['getMilestoneString'], 'Unlock every bobber style', 0), e['bobber_fish_left']), ' more unique fish'))))
        e.set('output', binary('+', e['output'], '</li></ul>'))
    e.set('output', binary('+', e['output'], '</div>'))
    if truth(binary('<', e['craft_count'], e['recipe_count'])):
        e.set('need', Array([]))
        for _key109 in keys(get(e['meta'], 'recipes')):
            e.set('id', _key109)
            if truth(call(get(get(e['meta'], 'recipes'), 'hasOwnProperty'), e['id'])):
                e.set('r', get(get(e['meta'], 'recipes'), e['id']))
                if truth(unary('!', call(get(e['known'], 'hasOwnProperty'), e['r']))):
                    call(get(e['need'], 'push'), binary('+', binary('+', '<li>', call(e['wikify'], e['r'])), '</li>'))
        put(e['meta'], 'hasDetails', True)
        e.set('output', binary('+', e['output'], binary('+', binary('+', binary('+', binary('+', '<div class="', get(e['meta'], 'anchor')), '_details '), get(e['meta'], 'det_class')), '">')))
        e.set('output', binary('+', e['output'], binary('+', binary('+', '<span class="need">Left to catch for achievements and bobber unlocks:<ol>', call(get(call(get(e['need'], 'sort')), 'join'), '')), '</ol></span></div>')))
    if truth(binary('>=', call(e['compareSemVer'], get(e['saveInfo'], 'version'), '1.6'), 0)):
        e.set('achieve_left', binary('-', e['recipe_count'], e['craft_count']))
        if truth((binary('>', e['bobber_fish_left'], e['achieve_left']) if truth(_logic110 := binary('<', e['bobbers_unlocked'], e['total_bobbers'])) else _logic110)):
            e.set('need', Array([]))
            for _key111 in keys(get(e['meta'], 'bobber')):
                e.set('id', _key111)
                if truth(call(get(get(e['meta'], 'bobber'), 'hasOwnProperty'), e['id'])):
                    e.set('r', get(get(e['meta'], 'bobber'), e['id']))
                    if truth(unary('!', call(get(e['known'], 'hasOwnProperty'), e['r']))):
                        call(get(e['need'], 'push'), binary('+', binary('+', '<li>', call(e['wikify'], e['r'])), '</li>'))
            put(e['meta'], 'hasDetails', True)
            e.set('output', binary('+', e['output'], binary('+', binary('+', binary('+', binary('+', '<div class="', get(e['meta'], 'anchor')), '_details '), get(e['meta'], 'det_class')), '">')))
            e.set('output', binary('+', e['output'], binary('+', binary('+', '<span class="need">Left to catch for bobber unlocks (don\'t need all):<ol>', call(get(call(get(e['need'], 'sort')), 'join'), '')), '</ol></span></div>')))
    return Array([e['output']])
    return U


def parseBasicShipping_112(parent, this, args):
    # Upstream checkup: 2304
    e = Env(parent)
    e.declare(['anchor', 'det_class', 'meta', 'output', 'playerOutput', 'sum_class', 'table', 'title', 'version'])
    e.local['arguments'] = Array(args)
    e.local['xmlDoc'] = (args[0] if len(args) > 0 and args[0] is not U else U)
    e.local['saveInfo'] = (args[1] if len(args) > 1 and args[1] is not U else U)
    e.set('title', 'Basic Shipping')
    e.set('anchor', call(e['makeAnchor'], e['title']))
    e.set('version', '1.2')
    e.set('sum_class', call(e['getSummaryClass'], e['saveInfo'], e['version']))
    e.set('det_class', call(e['getDetailsClass'], e['saveInfo'], e['version']))
    e.set('output', '')
    e.set('playerOutput', '')
    e.set('meta', Obj({'hasDetails': False, 'anchor': e['anchor'], 'sum_class': e['sum_class'], 'det_class': e['det_class']}))
    e.set('table', Array([]))
    put(e['meta'], 'recipes', table(9))
    if truth(binary('>=', call(e['compareSemVer'], get(e['saveInfo'], 'version'), '1.4'), 0)):
        put(get(e['meta'], 'recipes'), 807, 'Dinosaur Mayonnaise')
        put(get(e['meta'], 'recipes'), 812, 'Roe')
        put(get(e['meta'], 'recipes'), 445, 'Caviar')
        put(get(e['meta'], 'recipes'), 814, 'Squid Ink')
        put(get(e['meta'], 'recipes'), 815, 'Tea Leaves')
        put(get(e['meta'], 'recipes'), 447, 'Aged Roe')
        put(get(e['meta'], 'recipes'), 614, 'Green Tea')
        put(get(e['meta'], 'recipes'), 271, 'Unmilled Rice')
    if truth(binary('>=', call(e['compareSemVer'], get(e['saveInfo'], 'version'), '1.5'), 0)):
        put(get(e['meta'], 'recipes'), 91, 'Banana')
        put(get(e['meta'], 'recipes'), 289, 'Ostrich Egg')
        put(get(e['meta'], 'recipes'), 829, 'Ginger')
        put(get(e['meta'], 'recipes'), 830, 'Taro Root')
        put(get(e['meta'], 'recipes'), 832, 'Pineapple')
        put(get(e['meta'], 'recipes'), 834, 'Mango')
        put(get(e['meta'], 'recipes'), 848, 'Cinder Shard')
        put(get(e['meta'], 'recipes'), 851, 'Magma Cap')
        put(get(e['meta'], 'recipes'), 881, 'Bone Fragment')
        put(get(e['meta'], 'recipes'), 909, 'Radioactive Ore')
        put(get(e['meta'], 'recipes'), 910, 'Radioactive Bar')
    if truth(binary('>=', call(e['compareSemVer'], get(e['saveInfo'], 'version'), '1.6'), 0)):
        put(get(e['meta'], 'recipes'), 'Moss', 'Moss')
        put(get(e['meta'], 'recipes'), 'MysticSyrup', 'Mystic Syrup')
        put(get(e['meta'], 'recipes'), 'Raisins', 'Raisins')
        put(get(e['meta'], 'recipes'), 'DriedFruit', 'Dried Fruit')
        put(get(e['meta'], 'recipes'), 'DriedMushrooms', 'Dried Mushrooms')
        put(get(e['meta'], 'recipes'), 'Carrot', 'Carrot')
        put(get(e['meta'], 'recipes'), 'SummerSquash', 'Summer Squash')
        put(get(e['meta'], 'recipes'), 'Broccoli', 'Broccoli')
        put(get(e['meta'], 'recipes'), 'Powdermelon', 'Powdermelon')
        put(get(e['meta'], 'recipes'), 'SmokedFish', 'Smoked Fish')
    put(e['table'], 0, call(e['parsePlayerBasicShipping'], call(get(call(e['$'], e['xmlDoc']), 'find'), 'SaveGame > player'), e['saveInfo'], e['meta']))
    call(e['parseFarmhands'], e['xmlDoc'], e['saveInfo'], e['table'], e['parsePlayerBasicShipping'], e['meta'])
    e.set('playerOutput', binary('+', e['playerOutput'], call(e['printTranspose'], e['table'])))
    e.set('output', binary('+', binary('+', call(e['getSectionHeader'], e['saveInfo'], e['title'], e['anchor'], get(e['meta'], 'hasDetails'), e['version']), e['playerOutput']), call(e['getSectionFooter'])))
    return e['output']
    return U


def callback_114(parent, this, args):
    # Upstream checkup: 2503
    e = Env(parent)
    e.declare(['id', 'num'])
    e.local['arguments'] = Array(args)
    e.set('id', call(get(call(get(call(e['$'], this), 'find'), 'key > *'), 'text')))
    e.set('num', call(e['Number'], call(get(call(get(call(e['$'], this), 'find'), 'value > int'), 'text'))))
    if truth((binary('>', e['num'], 0) if truth(_logic115 := call(get(get(e['meta'], 'recipes'), 'hasOwnProperty'), e['id'])) else _logic115)):
        put(e['crafted'], get(get(e['meta'], 'recipes'), e['id']), e['num'])
        update_env(e, 'craft_count', 1, False)
    return U


def parsePlayerBasicShipping_113(parent, this, args):
    # Upstream checkup: 2491
    e = Env(parent)
    e.declare(['craft_count', 'crafted', 'id', 'need', 'output', 'pt_pct', 'r', 'recipe_count', 'umid'])
    e.local['arguments'] = Array(args)
    e.local['player'] = (args[0] if len(args) > 0 and args[0] is not U else U)
    e.local['saveInfo'] = (args[1] if len(args) > 1 and args[1] is not U else U)
    e.local['meta'] = (args[2] if len(args) > 2 and args[2] is not U else U)
    e.set('output', '')
    e.set('recipe_count', get(call(get(e['Object'], 'keys'), get(e['meta'], 'recipes')), 'length'))
    e.set('crafted', Obj({}))
    e.set('craft_count', 0)
    e.set('need', Array([]))
    e.set('umid', (call(get(call(get(call(e['$'], e['player']), 'children'), 'UniqueMultiplayerID'), 'text')) if truth(binary('>=', call(e['compareSemVer'], get(e['saveInfo'], 'version'), '1.3'), 0)) else get(e['saveInfo'], 'farmerId')))
    e.set('pt_pct', '')
    call(get(call(get(call(e['$'], e['player']), 'find'), 'basicShipped > item'), 'each'), Fn(callback_114, e))
    if truth(binary('>=', call(e['compareSemVer'], get(e['saveInfo'], 'version'), '1.5'), 0)):
        put(get(get(e['saveInfo'], 'perfectionTracker'), e['umid']), 'Shipping', Obj({'count': e['craft_count'], 'total': e['recipe_count']}))
        e.set('pt_pct', call(e['getPTLink'], binary('/', e['craft_count'], e['recipe_count']), True))
    e.set('output', binary('+', e['output'], binary('+', binary('+', binary('+', binary('+', '<div class="', get(e['meta'], 'anchor')), '_summary '), get(e['meta'], 'sum_class')), '">')))
    e.set('output', binary('+', e['output'], binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', '<span class="result">', call(get(call(get(call(e['$'], e['player']), 'children'), 'name'), 'html'))), ' has shipped '), e['craft_count']), ' of '), e['recipe_count']), ' basic items.'), e['pt_pct']), '</span><ul class="ach_list">\n')))
    e.set('output', binary('+', e['output'], '<li>'))
    e.set('output', binary('+', e['output'], (call(e['getAchieveString'], 'Full Shipment', 'ship every item', 1) if truth(binary('>=', e['craft_count'], e['recipe_count'])) else binary('+', binary('+', call(e['getAchieveString'], 'Full Shipment', 'ship every item', 0), binary('-', e['recipe_count'], e['craft_count'])), ' more'))))
    e.set('output', binary('+', e['output'], '</li></ul></div>'))
    if truth(binary('<', e['craft_count'], e['recipe_count'])):
        e.set('need', Array([]))
        for _key116 in keys(get(e['meta'], 'recipes')):
            e.set('id', _key116)
            if truth(call(get(get(e['meta'], 'recipes'), 'hasOwnProperty'), e['id'])):
                e.set('r', get(get(e['meta'], 'recipes'), e['id']))
                if truth(unary('!', call(get(e['crafted'], 'hasOwnProperty'), e['r']))):
                    call(get(e['need'], 'push'), binary('+', binary('+', '<li>', call(e['wikify'], e['r'])), '</li>'))
        put(e['meta'], 'hasDetails', True)
        e.set('output', binary('+', e['output'], binary('+', binary('+', binary('+', binary('+', '<div class="', get(e['meta'], 'anchor')), '_details '), get(e['meta'], 'det_class')), '">')))
        e.set('output', binary('+', e['output'], binary('+', binary('+', '<span class="need">Left to ship:<ol>', call(get(call(get(e['need'], 'sort')), 'join'), '')), '</ol></span></div>')))
    return Array([e['output']])
    return U


def parseCropShipping_117(parent, this, args):
    # Upstream checkup: 2540
    e = Env(parent)
    e.declare(['anchor', 'det_class', 'meta', 'output', 'playerOutput', 'sum_class', 'table', 'title', 'version'])
    e.local['arguments'] = Array(args)
    e.local['xmlDoc'] = (args[0] if len(args) > 0 and args[0] is not U else U)
    e.local['saveInfo'] = (args[1] if len(args) > 1 and args[1] is not U else U)
    e.set('title', 'Crop Shipping')
    e.set('anchor', call(e['makeAnchor'], e['title']))
    e.set('version', '1.2')
    e.set('sum_class', call(e['getSummaryClass'], e['saveInfo'], e['version']))
    e.set('det_class', call(e['getDetailsClass'], e['saveInfo'], e['version']))
    e.set('output', '')
    e.set('playerOutput', '')
    e.set('meta', Obj({'hasDetails': False, 'anchor': e['anchor'], 'sum_class': e['sum_class'], 'det_class': e['det_class']}))
    e.set('table', Array([]))
    put(e['meta'], 'poly_crops', table(10))
    put(e['meta'], 'mono_extras', Obj({'454': 'Ancient Fruit', '591': 'Tulip', '593': 'Summer Spangle', '595': 'Fairy Rose', '597': 'Blue Jazz'}))
    put(e['table'], 0, call(e['parsePlayerCropShipping'], call(get(call(e['$'], e['xmlDoc']), 'find'), 'SaveGame > player'), e['saveInfo'], e['meta']))
    call(e['parseFarmhands'], e['xmlDoc'], e['saveInfo'], e['table'], e['parsePlayerCropShipping'], e['meta'])
    e.set('playerOutput', binary('+', e['playerOutput'], call(e['printTranspose'], e['table'])))
    e.set('output', binary('+', binary('+', call(e['getSectionHeader'], e['saveInfo'], e['title'], e['anchor'], get(e['meta'], 'hasDetails'), e['version']), e['playerOutput']), call(e['getSectionFooter'])))
    return e['output']
    return U


def callback_119(parent, this, args):
    # Upstream checkup: 2616
    e = Env(parent)
    e.declare(['id', 'num'])
    e.local['arguments'] = Array(args)
    e.set('id', call(get(call(get(call(e['$'], this), 'find'), 'key > *'), 'text')))
    e.set('num', call(e['Number'], call(get(call(get(call(e['$'], this), 'find'), 'value > int'), 'text'))))
    if truth(call(get(get(e['meta'], 'poly_crops'), 'hasOwnProperty'), e['id'])):
        put(e['crafted'], get(get(e['meta'], 'poly_crops'), e['id']), e['num'])
        if truth(binary('>=', e['num'], 15)):
            update_env(e, 'craft_count', 1, False)
        if truth(binary('>', e['num'], e['max_ship'])):
            e.set('max_ship', e['num'])
            e.set('max_crop', get(get(e['meta'], 'poly_crops'), e['id']))
    else:
        if truth(call(get(get(e['meta'], 'mono_extras'), 'hasOwnProperty'), e['id'])):
            if truth(binary('>', e['num'], e['max_ship'])):
                e.set('max_ship', e['num'])
                e.set('max_crop', get(get(e['meta'], 'mono_extras'), e['id']))
    return U


def parsePlayerCropShipping_118(parent, this, args):
    # Upstream checkup: 2602
    e = Env(parent)
    e.declare(['craft_count', 'crafted', 'farmer', 'id', 'max_crop', 'max_ship', 'n', 'need', 'output', 'r', 'recipe_count'])
    e.local['arguments'] = Array(args)
    e.local['player'] = (args[0] if len(args) > 0 and args[0] is not U else U)
    e.local['saveInfo'] = (args[1] if len(args) > 1 and args[1] is not U else U)
    e.local['meta'] = (args[2] if len(args) > 2 and args[2] is not U else U)
    e.set('output', '')
    e.set('recipe_count', get(call(get(e['Object'], 'keys'), get(e['meta'], 'poly_crops')), 'length'))
    e.set('crafted', Obj({}))
    e.set('craft_count', 0)
    e.set('max_ship', 0)
    e.set('max_crop', 'of any crop')
    e.set('need', Array([]))
    e.set('farmer', call(get(call(get(call(e['$'], e['player']), 'children'), 'name'), 'html')))
    call(get(call(get(call(e['$'], e['player']), 'find'), 'basicShipped > item'), 'each'), Fn(callback_119, e))
    e.set('output', binary('+', e['output'], binary('+', binary('+', binary('+', binary('+', '<div class="', get(e['meta'], 'anchor')), '_summary '), get(e['meta'], 'sum_class')), '">')))
    e.set('output', binary('+', e['output'], (binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', '<span class="result">', e['farmer']), ' has shipped '), e['max_crop']), ' the most ('), e['max_ship']), ').</span>') if truth(binary('>', e['max_ship'], 0)) else binary('+', binary('+', '<span class="result">', e['farmer']), ' has not shipped any crops yet.</span>'))))
    e.set('output', binary('+', e['output'], '<ul class="ach_list"><li>\n'))
    e.set('output', binary('+', e['output'], (call(e['getAchieveString'], 'Monoculture', 'ship 300 of one crop', 1) if truth(binary('>=', e['max_ship'], 300)) else binary('+', binary('+', binary('+', call(e['getAchieveString'], 'Monoculture', 'ship 300 of one crop', 0), binary('-', 300, e['max_ship'])), ' more '), e['max_crop']))))
    e.set('output', binary('+', e['output'], '</li></ul>\n'))
    e.set('output', binary('+', e['output'], binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', '<span class="result">', e['farmer']), ' has shipped 15 items from '), e['craft_count']), ' of '), e['recipe_count']), ' different crops.</span><ul class="ach_list">\n<li>')))
    e.set('output', binary('+', e['output'], (call(e['getAchieveString'], 'Polyculture', 'ship 15 of each crop', 1) if truth(binary('>=', e['craft_count'], e['recipe_count'])) else binary('+', binary('+', binary('+', call(e['getAchieveString'], 'Polyculture', 'ship 15 of each crop', 0), ' more of '), binary('-', e['recipe_count'], e['craft_count'])), ' crops'))))
    e.set('output', binary('+', e['output'], '</li></ul></div>'))
    if truth(binary('<', e['craft_count'], e['recipe_count'])):
        e.set('need', Array([]))
        for _key120 in keys(get(e['meta'], 'poly_crops')):
            e.set('id', _key120)
            if truth(call(get(get(e['meta'], 'poly_crops'), 'hasOwnProperty'), e['id'])):
                e.set('r', get(get(e['meta'], 'poly_crops'), e['id']))
                if truth(unary('!', call(get(e['crafted'], 'hasOwnProperty'), e['r']))):
                    call(get(e['need'], 'push'), binary('+', binary('+', '<li>', call(e['wikify'], e['r'])), ' -- 15 more</li>'))
                else:
                    e.set('n', call(e['Number'], get(e['crafted'], e['r'])))
                    if truth(binary('<', e['n'], 15)):
                        call(get(e['need'], 'push'), binary('+', binary('+', binary('+', binary('+', '<li>', call(e['wikify'], e['r'])), ' -- '), binary('-', 15, e['n'])), ' more</li>'))
        put(e['meta'], 'hasDetails', True)
        e.set('output', binary('+', e['output'], binary('+', binary('+', binary('+', binary('+', '<div class="', get(e['meta'], 'anchor')), '_details '), get(e['meta'], 'det_class')), '">')))
        e.set('output', binary('+', e['output'], binary('+', binary('+', '<span class="need">Left to ship:<ol>', call(get(call(get(e['need'], 'sort')), 'join'), '')), '</ol></span></div>')))
    return Array([e['output']])
    return U


def parseSkills_121(parent, this, args):
    # Upstream checkup: 2670
    e = Env(parent)
    e.declare(['anchor', 'det_class', 'meta', 'output', 'playerOutput', 'sum_class', 'table', 'title', 'version'])
    e.local['arguments'] = Array(args)
    e.local['xmlDoc'] = (args[0] if len(args) > 0 and args[0] is not U else U)
    e.local['saveInfo'] = (args[1] if len(args) > 1 and args[1] is not U else U)
    e.set('title', 'Skills')
    e.set('output', '')
    e.set('anchor', call(e['makeAnchor'], e['title']))
    e.set('version', '1.2')
    e.set('sum_class', call(e['getSummaryClass'], e['saveInfo'], e['version']))
    e.set('det_class', call(e['getDetailsClass'], e['saveInfo'], e['version']))
    e.set('output', '')
    e.set('playerOutput', '')
    e.set('meta', Obj({'hasDetails': False, 'anchor': e['anchor'], 'sum_class': e['sum_class'], 'det_class': e['det_class']}))
    e.set('table', Array([]))
    (put(e['meta'], 'skills', Array(['Farming', 'Fishing', 'Foraging', 'Mining', 'Combat'])), put(e['meta'], 'next_level', Array([100, 380, 770, 1300, 2150, 3300, 4800, 6900, 10000, 15000])))[-1]
    put(e['table'], 0, call(e['parsePlayerSkills'], call(get(call(e['$'], e['xmlDoc']), 'find'), 'SaveGame > player'), e['saveInfo'], e['meta']))
    call(e['parseFarmhands'], e['xmlDoc'], e['saveInfo'], e['table'], e['parsePlayerSkills'], e['meta'])
    e.set('playerOutput', binary('+', e['playerOutput'], call(e['printTranspose'], e['table'])))
    e.set('output', binary('+', binary('+', call(e['getSectionHeader'], e['saveInfo'], e['title'], e['anchor'], get(e['meta'], 'hasDetails'), e['version']), e['playerOutput']), call(e['getSectionFooter'])))
    return e['output']
    return U


def parsePlayerSkills_122(parent, this, args):
    # Upstream checkup: 2692
    e = Env(parent)
    e.declare(['count', 'i', 'isMale', 'j', 'level', 'masteryXP', 'need', 'num', 'output', 'pt_level', 'pt_pct', 'title', 'umid', 'xp'])
    e.local['arguments'] = Array(args)
    e.local['player'] = (args[0] if len(args) > 0 and args[0] is not U else U)
    e.local['saveInfo'] = (args[1] if len(args) > 1 and args[1] is not U else U)
    e.local['meta'] = (args[2] if len(args) > 2 and args[2] is not U else U)
    e.set('output', '')
    e.set('xp', Obj({}))
    e.set('level', 10)
    e.set('count', 0)
    e.set('umid', (call(get(call(get(call(e['$'], e['player']), 'children'), 'UniqueMultiplayerID'), 'text')) if truth(binary('>=', call(e['compareSemVer'], get(e['saveInfo'], 'version'), '1.3'), 0)) else get(e['saveInfo'], 'farmerId')))
    e.set('isMale', binary('===', call(get(call(get(call(e['$'], e['player']), 'children'), 'isMale'), 'text')), 'true'))
    e.set('pt_pct', '')
    e.set('pt_level', 0)
    e.set('title', '')
    e.set('masteryXP', 0)
    e.set('need', Array([]))
    e.set('i', 0)
    while truth(binary('<', e['i'], get(get(e['meta'], 'skills'), 'length'))):
        e.set('num', get(get(get(get(e['saveInfo'], 'data'), e['umid']), 'experiencePoints'), e['i']))
        put(e['xp'], get(get(e['meta'], 'skills'), e['i']), e['num'])
        if truth(binary('<', e['num'], 15000)):
            e.set('j', 0)
            while truth(binary('<', e['j'], 10)):
                if truth(binary('>', get(get(e['meta'], 'next_level'), e['j']), e['num'])):
                    e.set('level', e['j'])
                    break
                update_env(e, 'j', 1, False)
            call(get(e['need'], 'push'), binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', '<li>', call(e['wikify'], get(get(e['meta'], 'skills'), e['i']))), ' (level '), e['level']), ') -- need '), call(e['addCommas'], binary('-', get(get(e['meta'], 'next_level'), e['level']), e['num']))), ' more xp to next level and '), call(e['addCommas'], binary('-', 15000, e['num']))), ' more xp to max</li>\n'))
        else:
            update_env(e, 'count', 1, False)
        update_env(e, 'i', 1, False)
    e.set('pt_level', call(get(e['Math'], 'floor'), binary('/', binary('+', binary('+', binary('+', binary('+', binary('+', call(e['Number'], call(get(call(get(call(e['$'], e['player']), 'find'), 'farmingLevel'), 'text'))), call(e['Number'], call(get(call(get(call(e['$'], e['player']), 'find'), 'miningLevel'), 'text')))), call(e['Number'], call(get(call(get(call(e['$'], e['player']), 'find'), 'combatLevel'), 'text')))), call(e['Number'], call(get(call(get(call(e['$'], e['player']), 'find'), 'foragingLevel'), 'text')))), call(e['Number'], call(get(call(get(call(e['$'], e['player']), 'find'), 'fishingLevel'), 'text')))), call(e['Number'], call(get(call(get(call(e['$'], e['player']), 'find'), 'luckLevel'), 'text')))), 2)))
    if truth(binary('>=', call(e['compareSemVer'], get(e['saveInfo'], 'version'), '1.5'), 0)):
        e.set('pt_pct', call(e['getPTLink'], binary('+', binary('/', e['pt_level'], 0.25), '%')))
        put(get(get(e['saveInfo'], 'perfectionTracker'), e['umid']), 'Skills', Obj({'count': e['pt_level'], 'total': 25}))
    _switch123 = e['pt_level']
    _switch123_index = -1
    if _switch123_index < 0 and strict_equal(_switch123, 0): _switch123_index = 0
    if _switch123_index < 0 and strict_equal(_switch123, 1): _switch123_index = 1
    if _switch123_index < 0 and strict_equal(_switch123, 2): _switch123_index = 2
    if _switch123_index < 0 and strict_equal(_switch123, 3): _switch123_index = 3
    if _switch123_index < 0 and strict_equal(_switch123, 4): _switch123_index = 4
    if _switch123_index < 0 and strict_equal(_switch123, 5): _switch123_index = 5
    if _switch123_index < 0 and strict_equal(_switch123, 6): _switch123_index = 6
    if _switch123_index < 0 and strict_equal(_switch123, 7): _switch123_index = 7
    if _switch123_index < 0 and strict_equal(_switch123, 8): _switch123_index = 8
    if _switch123_index < 0 and strict_equal(_switch123, 9): _switch123_index = 9
    if _switch123_index < 0 and strict_equal(_switch123, 10): _switch123_index = 10
    if _switch123_index < 0 and strict_equal(_switch123, 11): _switch123_index = 11
    if _switch123_index < 0 and strict_equal(_switch123, 12): _switch123_index = 12
    if _switch123_index < 0 and strict_equal(_switch123, 13): _switch123_index = 13
    if _switch123_index < 0 and strict_equal(_switch123, 14): _switch123_index = 14
    if _switch123_index < 0 and strict_equal(_switch123, 15): _switch123_index = 15
    if _switch123_index < 0 and strict_equal(_switch123, 16): _switch123_index = 16
    if _switch123_index < 0 and strict_equal(_switch123, 17): _switch123_index = 17
    if _switch123_index < 0 and strict_equal(_switch123, 18): _switch123_index = 18
    if _switch123_index < 0 and strict_equal(_switch123, 19): _switch123_index = 19
    if _switch123_index < 0 and strict_equal(_switch123, 20): _switch123_index = 20
    if _switch123_index < 0 and strict_equal(_switch123, 21): _switch123_index = 21
    if _switch123_index < 0 and strict_equal(_switch123, 22): _switch123_index = 22
    if _switch123_index < 0 and strict_equal(_switch123, 23): _switch123_index = 23
    if _switch123_index < 0 and strict_equal(_switch123, 24): _switch123_index = 24
    if _switch123_index < 0 and strict_equal(_switch123, 25): _switch123_index = 25
    if _switch123_index < 0 and strict_equal(_switch123, 26): _switch123_index = 26
    if _switch123_index < 0 and strict_equal(_switch123, 27): _switch123_index = 27
    if _switch123_index < 0 and strict_equal(_switch123, 28): _switch123_index = 28
    if _switch123_index < 0 and strict_equal(_switch123, 29): _switch123_index = 29
    if _switch123_index < 0: _switch123_index = 30
    while True:
        if 0 <= _switch123_index <= 0:
            pass
        if 0 <= _switch123_index <= 1:
            pass
        if 0 <= _switch123_index <= 2:
            e.set('title', 'Newcomer')
            break
        if 0 <= _switch123_index <= 3:
            pass
        if 0 <= _switch123_index <= 4:
            e.set('title', 'Greenhorn')
            break
        if 0 <= _switch123_index <= 5:
            pass
        if 0 <= _switch123_index <= 6:
            e.set('title', 'Bumpkin')
            break
        if 0 <= _switch123_index <= 7:
            pass
        if 0 <= _switch123_index <= 8:
            e.set('title', 'Cowpoke')
            break
        if 0 <= _switch123_index <= 9:
            pass
        if 0 <= _switch123_index <= 10:
            e.set('title', 'Farmhand')
            break
        if 0 <= _switch123_index <= 11:
            pass
        if 0 <= _switch123_index <= 12:
            e.set('title', 'Tiller')
            break
        if 0 <= _switch123_index <= 13:
            pass
        if 0 <= _switch123_index <= 14:
            e.set('title', 'Smallholder')
            break
        if 0 <= _switch123_index <= 15:
            pass
        if 0 <= _switch123_index <= 16:
            e.set('title', 'Sodbuster')
            break
        if 0 <= _switch123_index <= 17:
            pass
        if 0 <= _switch123_index <= 18:
            e.set('title', binary('+', 'Farm', ('boy' if truth(e['isMale']) else 'girl')))
            break
        if 0 <= _switch123_index <= 19:
            pass
        if 0 <= _switch123_index <= 20:
            e.set('title', 'Granger')
            break
        if 0 <= _switch123_index <= 21:
            pass
        if 0 <= _switch123_index <= 22:
            e.set('title', 'Planter')
            break
        if 0 <= _switch123_index <= 23:
            pass
        if 0 <= _switch123_index <= 24:
            e.set('title', 'Rancher')
            break
        if 0 <= _switch123_index <= 25:
            pass
        if 0 <= _switch123_index <= 26:
            e.set('title', 'Farmer')
            break
        if 0 <= _switch123_index <= 27:
            pass
        if 0 <= _switch123_index <= 28:
            e.set('title', 'Agriculturist')
            break
        if 0 <= _switch123_index <= 29:
            e.set('title', 'Cropmaster')
            break
        if 0 <= _switch123_index <= 30:
            e.set('title', 'Farm King')
        break
    e.set('output', binary('+', e['output'], binary('+', binary('+', binary('+', binary('+', '<div class="', get(e['meta'], 'anchor')), '_summary '), get(e['meta'], 'sum_class')), '">')))
    e.set('output', binary('+', e['output'], binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', '<span class="result">', get(get(e['saveInfo'], 'players'), e['umid'])), ' is <a href="https://stardewvalleywiki.com/Skills#Skill-Based_Title">Farmer Level</a> '), e['pt_level']), ' with title '), e['title']), '.'), e['pt_pct']), '</span><br />')))
    e.set('output', binary('+', e['output'], binary('+', binary('+', binary('+', binary('+', '<span class="result">', get(get(e['saveInfo'], 'players'), e['umid'])), ' has reached level 10 in '), e['count']), ' of 5 skills.</span><br />')))
    e.set('output', binary('+', e['output'], '<ul class="ach_list"><li>'))
    e.set('output', binary('+', e['output'], (call(e['getAchieveString'], 'Singular Talent', 'level 10 in a skill', 1) if truth(binary('>=', e['count'], 1)) else binary('+', binary('+', call(e['getAchieveString'], 'Singular Talent', 'level 10 in a skill', 0), binary('-', 1, e['count'])), ' more'))))
    e.set('output', binary('+', e['output'], '</li>\n<li>'))
    e.set('output', binary('+', e['output'], (call(e['getAchieveString'], 'Master of the Five Ways', 'level 10 in every skill', 1) if truth(binary('>=', e['count'], 5)) else binary('+', binary('+', call(e['getAchieveString'], 'Master of the Five Ways', 'level 10 in every skill', 0), binary('-', 5, e['count'])), ' more'))))
    e.set('output', binary('+', e['output'], '</li></ul></div>'))
    if truth(binary('>', get(e['need'], 'length'), 0)):
        put(e['meta'], 'hasDetails', True)
        e.set('output', binary('+', e['output'], binary('+', binary('+', binary('+', binary('+', '<div class="', get(e['meta'], 'anchor')), '_details '), get(e['meta'], 'det_class')), '">')))
        e.set('output', binary('+', e['output'], binary('+', binary('+', '<span class="need">Skills left:<ol>', call(get(call(get(e['need'], 'sort')), 'join'), '')), '</ol></span></div>')))
    return Array([e['output']])
    return U


def parseSkillMastery_124(parent, this, args):
    # Upstream checkup: 2805
    e = Env(parent)
    e.declare(['anchor', 'det_class', 'meta', 'output', 'playerOutput', 'sum_class', 'table', 'title', 'version'])
    e.local['arguments'] = Array(args)
    e.local['xmlDoc'] = (args[0] if len(args) > 0 and args[0] is not U else U)
    e.local['saveInfo'] = (args[1] if len(args) > 1 and args[1] is not U else U)
    e.set('title', 'Skill Mastery')
    e.set('output', '')
    e.set('anchor', call(e['makeAnchor'], e['title']))
    e.set('version', '1.6')
    e.set('sum_class', call(e['getSummaryClass'], e['saveInfo'], e['version']))
    e.set('det_class', call(e['getDetailsClass'], e['saveInfo'], e['version']))
    e.set('output', '')
    e.set('playerOutput', '')
    e.set('meta', Obj({'hasDetails': False, 'anchor': e['anchor'], 'sum_class': e['sum_class'], 'det_class': e['det_class']}))
    e.set('table', Array([]))
    put(e['meta'], 'skills', Array(['Farming', 'Fishing', 'Foraging', 'Mining', 'Combat']))
    put(e['meta'], 'nextLevel', Array([0, 10000, 25000, 45000, 70000, 100000]))
    if truth(binary('<', call(e['compareSemVer'], get(e['saveInfo'], 'version'), e['version']), 0)):
        return ''
    put(e['table'], 0, call(e['parsePlayerSkillMastery'], call(get(call(e['$'], e['xmlDoc']), 'find'), 'SaveGame > player'), e['saveInfo'], e['meta']))
    call(e['parseFarmhands'], e['xmlDoc'], e['saveInfo'], e['table'], e['parsePlayerSkillMastery'], e['meta'])
    e.set('playerOutput', binary('+', e['playerOutput'], call(e['printTranspose'], e['table'])))
    e.set('output', binary('+', binary('+', call(e['getSectionHeader'], e['saveInfo'], e['title'], e['anchor'], get(e['meta'], 'hasDetails'), e['version']), e['playerOutput']), call(e['getSectionFooter'])))
    return e['output']
    return U


def parsePlayerSkillMastery_125(parent, this, args):
    # Upstream checkup: 2830
    e = Env(parent)
    e.declare(['i', 'id', 'masteryNextLvl', 'masteryNextXP', 'masteryXP', 'maxCount', 'needPerk', 'num', 'output', 'perkCount', 'umid', 'unchosen', 'xp'])
    e.local['arguments'] = Array(args)
    e.local['player'] = (args[0] if len(args) > 0 and args[0] is not U else U)
    e.local['saveInfo'] = (args[1] if len(args) > 1 and args[1] is not U else U)
    e.local['meta'] = (args[2] if len(args) > 2 and args[2] is not U else U)
    e.set('output', '')
    e.set('xp', Obj({}))
    e.set('i', 0)
    e.set('maxCount', 0)
    e.set('perkCount', 0)
    e.set('umid', call(get(call(get(call(e['$'], e['player']), 'children'), 'UniqueMultiplayerID'), 'text')))
    e.set('masteryXP', 0)
    e.set('unchosen', 0)
    e.set('needPerk', Array([]))
    if truth(call(get(get(get(get(e['saveInfo'], 'data'), e['umid']), 'stats'), 'hasOwnProperty'), 'MasteryExp')):
        e.set('masteryXP', get(get(get(get(e['saveInfo'], 'data'), e['umid']), 'stats'), 'MasteryExp'))
    if truth(binary('<', e['masteryXP'], 100000)):
        e.set('i', 1)
        while truth(binary('<=', e['i'], 5)):
            if truth(binary('<', e['masteryXP'], get(get(e['meta'], 'nextLevel'), e['i']))):
                e.set('masteryNextLvl', e['i'])
                break
            update_env(e, 'i', 1, False)
        e.set('masteryNextXP', get(get(e['meta'], 'nextLevel'), e['masteryNextLvl']))
    e.set('i', 0)
    while truth(binary('<', e['i'], get(get(e['meta'], 'skills'), 'length'))):
        e.set('id', binary('+', 'mastery_', e['i']))
        if truth(call(get(get(get(get(e['saveInfo'], 'data'), e['umid']), 'stats'), 'hasOwnProperty'), e['id'])):
            update_env(e, 'perkCount', 1, False)
        else:
            call(get(e['needPerk'], 'push'), binary('+', binary('+', '<li>', get(get(e['meta'], 'skills'), e['i'])), '</li>'))
        if truth(binary('>=', get(get(get(get(e['saveInfo'], 'data'), e['umid']), 'experiencePoints'), e['i']), 15000)):
            update_env(e, 'maxCount', 1, False)
        update_env(e, 'i', 1, False)
    if truth(binary('>', e['masteryNextLvl'], binary('+', e['perkCount'], 1))):
        e.set('unchosen', binary('-', binary('-', e['masteryNextLvl'], e['perkCount']), 1))
    e.set('output', binary('+', e['output'], binary('+', binary('+', binary('+', binary('+', '<div class="', get(e['meta'], 'anchor')), '_summary '), get(e['meta'], 'sum_class')), '">')))
    e.set('output', binary('+', e['output'], binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', '<span class="result">', get(get(e['saveInfo'], 'players'), e['umid'])), ' has maxed '), e['maxCount']), ' of '), get(get(e['meta'], 'skills'), 'length')), ' skills.</span><br />')))
    e.set('output', binary('+', e['output'], '<ul class="ach_list"><li>\n'))
    e.set('output', binary('+', e['output'], (call(e['getMilestoneString'], 'Gain access to the Mastery Cave', 1) if truth(binary('>=', e['maxCount'], 5)) else binary('+', binary('+', call(e['getMilestoneString'], 'Gain access to the Mastery Cave', 0), binary('-', get(get(e['meta'], 'skills'), 'length'), e['maxCount'])), ' more maxed skills -- <a href="#sec_Skills">see above for needs</a>'))))
    e.set('output', binary('+', e['output'], binary('+', binary('+', binary('+', binary('+', '</li></ul><span class="result">', get(get(e['saveInfo'], 'players'), e['umid'])), ' has '), call(e['addCommas'], e['masteryXP'])), ' mastery xp.</span><br />')))
    e.set('output', binary('+', e['output'], '<ul class="ach_list"><li>\n'))
    e.set('output', binary('+', e['output'], (call(e['getMilestoneString'], 'Reach 100,000 mastery xp', 1) if truth(binary('>=', e['masteryXP'], 100000)) else binary('+', binary('+', binary('+', binary('+', call(e['getMilestoneString'], 'Reach 100,000 mastery xp', 0), call(e['addCommas'], binary('-', e['masteryNextXP'], e['masteryXP']))), ' more xp for next perk unlock and '), call(e['addCommas'], binary('-', 100000, e['masteryXP']))), ' more xp overall'))))
    e.set('output', binary('+', e['output'], binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', '</li></ul><span class="result">', get(get(e['saveInfo'], 'players'), e['umid'])), ' has selected '), e['perkCount']), ' of '), get(get(e['meta'], 'skills'), 'length')), ' mastery perks.</span><br />')))
    e.set('output', binary('+', e['output'], '<ul class="ach_list"><li>\n'))
    e.set('output', binary('+', e['output'], (call(e['getMilestoneString'], 'Acquire all mastery perks', 1) if truth(binary('>=', e['perkCount'], 5)) else binary('+', binary('+', call(e['getMilestoneString'], 'Acquire all mastery perks', 0), binary('-', get(get(e['meta'], 'skills'), 'length'), e['perkCount'])), ' more'))))
    e.set('output', binary('+', e['output'], (binary('+', binary('+', ' including ', e['unchosen']), ' available but unselected.') if truth((binary('>', e['unchosen'], 0) if truth(_logic126 := binary('<', e['perkCount'], 5)) else _logic126)) else '.')))
    e.set('output', binary('+', e['output'], '</li></ul></div>'))
    if truth(binary('>', get(e['needPerk'], 'length'), 0)):
        put(e['meta'], 'hasDetails', True)
        e.set('output', binary('+', e['output'], binary('+', binary('+', binary('+', binary('+', '<div class="', get(e['meta'], 'anchor')), '_details '), get(e['meta'], 'det_class')), '">')))
        e.set('output', binary('+', e['output'], binary('+', binary('+', '<span class="need">Perks left:<ol>', call(get(call(get(e['needPerk'], 'sort')), 'join'), '')), '</ol></span></div>')))
    return Array([e['output']])
    return U


def callback_128(parent, this, args):
    # Upstream checkup: 3016
    e = Env(parent)
    e.declare(['id'])
    e.local['arguments'] = Array(args)
    e.set('id', call(e['Number'], call(get(call(get(call(e['$'], this), 'find'), 'value > *'), 'text'))))
    if truth((_logic129 if truth(_logic129 := call(get(get(e['meta'], 'artifacts'), 'hasOwnProperty'), e['id'])) else call(get(get(e['meta'], 'minerals'), 'hasOwnProperty'), e['id']))):
        put(get(e['meta'], 'donated'), e['id'], 1)
    return U


def parseMuseum_127(parent, this, args):
    # Upstream checkup: 2897
    e = Env(parent)
    e.declare(['anchor', 'artifact_count', 'det_class', 'donated_count', 'intro', 'meta', 'mineral_count', 'museum', 'museum_count', 'output', 'playerOutput', 'sum_class', 'table', 'title', 'version'])
    e.local['arguments'] = Array(args)
    e.local['xmlDoc'] = (args[0] if len(args) > 0 and args[0] is not U else U)
    e.local['saveInfo'] = (args[1] if len(args) > 1 and args[1] is not U else U)
    e.set('title', 'Museum Collection')
    e.set('anchor', call(e['makeAnchor'], e['title']))
    e.set('version', '1.2')
    e.set('sum_class', call(e['getSummaryClass'], e['saveInfo'], e['version']))
    e.set('det_class', call(e['getDetailsClass'], e['saveInfo'], e['version']))
    e.set('output', '')
    e.set('playerOutput', '')
    e.set('meta', Obj({'hasDetails': False, 'anchor': e['anchor'], 'sum_class': e['sum_class'], 'det_class': e['det_class']}))
    e.set('table', Array([]))
    e.set('museum', call(get(call(e['$'], e['xmlDoc']), 'find'), binary('+', binary('+', 'locations > GameLocation[', get(e['saveInfo'], 'ns_prefix')), "\\:type='LibraryMuseum']")))
    put(e['meta'], 'artifacts', table(11))
    put(e['meta'], 'minerals', table(12))
    put(e['meta'], 'donated', Obj({}))
    e.set('artifact_count', get(call(get(e['Object'], 'keys'), get(e['meta'], 'artifacts')), 'length'))
    e.set('mineral_count', get(call(get(e['Object'], 'keys'), get(e['meta'], 'minerals')), 'length'))
    e.set('donated_count', 0)
    e.set('museum_count', binary('+', e['artifact_count'], e['mineral_count']))
    call(get(call(get(call(e['$'], e['museum']), 'find'), 'museumPieces > item'), 'each'), Fn(callback_128, e))
    e.set('donated_count', get(call(get(e['Object'], 'keys'), get(e['meta'], 'donated')), 'length'))
    e.set('output', binary('+', binary('+', binary('+', binary('+', '<div class="', get(e['meta'], 'anchor')), '_summary '), get(e['meta'], 'sum_class')), '">'))
    if truth(binary('>', get(e['saveInfo'], 'numPlayers'), 1)):
        e.set('intro', binary('+', binary('+', 'Inhabitants of ', get(e['saveInfo'], 'farmName')), ' Farm have'))
    else:
        e.set('intro', binary('+', get(get(e['saveInfo'], 'players'), get(e['saveInfo'], 'farmerId')), ' has'))
    e.set('output', binary('+', e['output'], binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', '<span class="result">', e['intro']), ' donated '), e['donated_count']), ' of '), e['museum_count']), ' items to the museum.</span><ul class="ach_list">\n')))
    e.set('output', binary('+', e['output'], '<li>'))
    e.set('output', binary('+', e['output'], (call(e['getAchieveString'], 'Treasure Trove', 'donate 40 items', 1) if truth(binary('>=', e['donated_count'], 40)) else binary('+', binary('+', call(e['getAchieveString'], 'Treasure Trove', 'donate 40 items', 0), binary('-', 40, e['donated_count'])), ' more'))))
    e.set('output', binary('+', e['output'], '</li>\n<li>'))
    e.set('output', binary('+', e['output'], (call(e['getMilestoneString'], 'Donate enough items (60) to get the Rusty Key', 1) if truth(binary('>=', e['donated_count'], 60)) else binary('+', binary('+', call(e['getMilestoneString'], 'Donate enough items (60) to get the Rusty Key', 0), binary('-', 60, e['donated_count'])), ' more'))))
    e.set('output', binary('+', e['output'], '</li>\n<li>'))
    e.set('output', binary('+', e['output'], (call(e['getAchieveString'], 'A Complete Collection', 'donate every item', 1) if truth(binary('>=', e['donated_count'], e['museum_count'])) else binary('+', binary('+', call(e['getAchieveString'], 'A Complete Collection', 'donate every item', 0), binary('-', e['museum_count'], e['donated_count'])), ' more'))))
    e.set('output', binary('+', e['output'], '</li></ul></div>'))
    if truth(binary('<', e['donated_count'], e['museum_count'])):
        put(e['meta'], 'hasDetails', True)
        e.set('output', binary('+', e['output'], binary('+', binary('+', binary('+', binary('+', '<div class="', get(e['meta'], 'anchor')), '_details '), get(e['meta'], 'det_class')), '">')))
        e.set('output', binary('+', e['output'], '<span class="need">See below for items left to donate</span><br /><br /></div>'))
    put(e['table'], 0, call(e['parsePlayerMuseum'], call(get(call(e['$'], e['xmlDoc']), 'find'), 'SaveGame > player'), e['saveInfo'], e['meta']))
    call(e['parseFarmhands'], e['xmlDoc'], e['saveInfo'], e['table'], e['parsePlayerMuseum'], e['meta'])
    e.set('playerOutput', binary('+', e['playerOutput'], call(e['printTranspose'], e['table'])))
    e.set('output', binary('+', binary('+', binary('+', call(e['getSectionHeader'], e['saveInfo'], e['title'], e['anchor'], get(e['meta'], 'hasDetails'), e['version']), e['output']), e['playerOutput']), call(e['getSectionFooter'])))
    return e['output']
    return U


def callback_131(parent, this, args):
    # Upstream checkup: 3072
    e = Env(parent)
    e.declare(['id', 'num'])
    e.local['arguments'] = Array(args)
    e.set('id', call(get(call(get(call(e['$'], this), 'find'), 'key > *'), 'text')))
    e.set('num', call(e['Number'], call(get(call(get(call(get(call(e['$'], this), 'find'), 'value > ArrayOfInt > int'), 'first')), 'text'))))
    if truth((binary('>', e['num'], 0) if truth(_logic132 := call(get(get(e['meta'], 'artifacts'), 'hasOwnProperty'), e['id'])) else _logic132)):
        put(e['found'], e['id'], e['num'])
        update_env(e, 'found_art', 1, False)
    return U


def callback_133(parent, this, args):
    # Upstream checkup: 3080
    e = Env(parent)
    e.declare(['id', 'num'])
    e.local['arguments'] = Array(args)
    e.set('id', call(get(call(get(call(e['$'], this), 'find'), 'key > *'), 'text')))
    e.set('num', call(e['Number'], call(get(call(get(call(e['$'], this), 'find'), 'value > int'), 'text'))))
    if truth((binary('>', e['num'], 0) if truth(_logic134 := call(get(get(e['meta'], 'minerals'), 'hasOwnProperty'), e['id'])) else _logic134)):
        put(e['found'], e['id'], e['num'])
        update_env(e, 'found_min', 1, False)
    return U


def parsePlayerMuseum_130(parent, this, args):
    # Upstream checkup: 3056
    e = Env(parent)
    e.declare(['artifact_count', 'donated_count', 'farmer', 'found', 'found_art', 'found_min', 'id', 'mineral_count', 'museum_count', 'need', 'need_art', 'need_min', 'output', 'r'])
    e.local['arguments'] = Array(args)
    e.local['player'] = (args[0] if len(args) > 0 and args[0] is not U else U)
    e.local['saveInfo'] = (args[1] if len(args) > 1 and args[1] is not U else U)
    e.local['meta'] = (args[2] if len(args) > 2 and args[2] is not U else U)
    e.set('output', '')
    e.set('donated_count', get(call(get(e['Object'], 'keys'), get(e['meta'], 'donated')), 'length'))
    e.set('artifact_count', get(call(get(e['Object'], 'keys'), get(e['meta'], 'artifacts')), 'length'))
    e.set('mineral_count', get(call(get(e['Object'], 'keys'), get(e['meta'], 'minerals')), 'length'))
    e.set('museum_count', binary('+', e['artifact_count'], e['mineral_count']))
    e.set('found', Obj({}))
    e.set('found_art', 0)
    e.set('found_min', 0)
    e.set('need_art', Array([]))
    e.set('need_min', Array([]))
    e.set('need', Array([]))
    e.set('farmer', call(get(call(get(call(e['$'], e['player']), 'children'), 'name'), 'html')))
    call(get(call(get(call(e['$'], e['player']), 'find'), 'archaeologyFound > item'), 'each'), Fn(callback_131, e))
    call(get(call(get(call(e['$'], e['player']), 'find'), 'mineralsFound > item'), 'each'), Fn(callback_133, e))
    e.set('output', binary('+', e['output'], binary('+', binary('+', binary('+', binary('+', '<div class="', get(e['meta'], 'anchor')), '_summary '), get(e['meta'], 'sum_class')), '">')))
    e.set('output', binary('+', e['output'], binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', '<span class="result">', e['farmer']), ' has found '), e['found_art']), ' of '), e['artifact_count']), ' artifacts.</span><br />\n')))
    e.set('output', binary('+', e['output'], binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', '<span class="result">', e['farmer']), ' has found '), e['found_min']), ' of '), e['mineral_count']), ' minerals.</span><ul class="ach_list">\n')))
    e.set('output', binary('+', e['output'], '<li>'))
    e.set('output', binary('+', e['output'], '</li>\n<li>'))
    e.set('output', binary('+', e['output'], (call(e['getMilestoneString'], 'All artifacts found', 1) if truth(binary('>=', e['found_art'], e['artifact_count'])) else binary('+', binary('+', call(e['getMilestoneString'], 'All artifacts found', 0), binary('-', e['artifact_count'], e['found_art'])), ' more'))))
    e.set('output', binary('+', e['output'], '</li>\n<li>'))
    e.set('output', binary('+', e['output'], (call(e['getMilestoneString'], 'All minerals found', 1) if truth(binary('>=', e['found_min'], e['mineral_count'])) else binary('+', binary('+', call(e['getMilestoneString'], 'All minerals found', 0), binary('-', e['mineral_count'], e['found_min'])), ' more'))))
    e.set('output', binary('+', e['output'], '</li></ul></div>'))
    if truth((_logic135 if truth(_logic135 := binary('<', e['donated_count'], e['museum_count'])) else binary('<', binary('+', e['found_art'], e['found_min']), e['museum_count']))):
        for _key136 in keys(get(e['meta'], 'artifacts')):
            e.set('id', _key136)
            if truth(call(get(get(e['meta'], 'artifacts'), 'hasOwnProperty'), e['id'])):
                e.set('r', get(get(e['meta'], 'artifacts'), e['id']))
                e.set('need', Array([]))
                if truth(unary('!', call(get(e['found'], 'hasOwnProperty'), e['id']))):
                    call(get(e['need'], 'push'), 'found')
                if truth(unary('!', call(get(get(e['meta'], 'donated'), 'hasOwnProperty'), e['id']))):
                    call(get(e['need'], 'push'), 'donated')
                if truth(binary('>', get(e['need'], 'length'), 0)):
                    call(get(e['need_art'], 'push'), binary('+', binary('+', binary('+', binary('+', '<li>', call(e['wikify'], e['r'])), ' -- not '), call(get(e['need'], 'join'), ' or ')), '</li>'))
        for _key137 in keys(get(e['meta'], 'minerals')):
            e.set('id', _key137)
            if truth(call(get(get(e['meta'], 'minerals'), 'hasOwnProperty'), e['id'])):
                e.set('r', get(get(e['meta'], 'minerals'), e['id']))
                e.set('need', Array([]))
                if truth(unary('!', call(get(e['found'], 'hasOwnProperty'), e['id']))):
                    call(get(e['need'], 'push'), 'found')
                if truth(unary('!', call(get(get(e['meta'], 'donated'), 'hasOwnProperty'), e['id']))):
                    call(get(e['need'], 'push'), 'donated')
                if truth(binary('>', get(e['need'], 'length'), 0)):
                    call(get(e['need_min'], 'push'), binary('+', binary('+', binary('+', binary('+', '<li>', call(e['wikify'], e['r'])), ' -- not '), call(get(e['need'], 'join'), ' or ')), '</li>'))
        put(e['meta'], 'hasDetails', True)
        e.set('output', binary('+', e['output'], binary('+', binary('+', binary('+', binary('+', '<div class="', get(e['meta'], 'anchor')), '_details '), get(e['meta'], 'det_class')), '">')))
        e.set('output', binary('+', e['output'], '<span class="need">Items left:<ul>'))
        if truth(binary('>', get(e['need_art'], 'length'), 0)):
            e.set('output', binary('+', e['output'], binary('+', binary('+', '<li>Artifacts<ol>', call(get(call(get(e['need_art'], 'sort')), 'join'), '')), '</ol></li>\n')))
        if truth(binary('>', get(e['need_min'], 'length'), 0)):
            e.set('output', binary('+', e['output'], binary('+', binary('+', '<li>Minerals<ol>', call(get(call(get(e['need_min'], 'sort')), 'join'), '')), '</ol></li>\n')))
        e.set('output', binary('+', e['output'], '</ul></span></div>'))
    return Array([e['output']])
    return U


def parseMonsters_138(parent, this, args):
    # Upstream checkup: 3148
    e = Env(parent)
    e.declare(['anchor', 'det_class', 'meta', 'output', 'playerOutput', 'sum_class', 'table', 'title', 'version'])
    e.local['arguments'] = Array(args)
    e.local['xmlDoc'] = (args[0] if len(args) > 0 and args[0] is not U else U)
    e.local['saveInfo'] = (args[1] if len(args) > 1 and args[1] is not U else U)
    e.set('title', 'Monster Hunting')
    e.set('anchor', call(e['makeAnchor'], e['title']))
    e.set('version', '1.2')
    e.set('sum_class', call(e['getSummaryClass'], e['saveInfo'], e['version']))
    e.set('det_class', call(e['getDetailsClass'], e['saveInfo'], e['version']))
    e.set('output', '')
    e.set('playerOutput', '')
    e.set('meta', Obj({'hasDetails': False, 'anchor': e['anchor'], 'sum_class': e['sum_class'], 'det_class': e['det_class']}))
    e.set('table', Array([]))
    put(e['meta'], 'goals', Obj({'Slimes': 1000, 'Void Spirits': 150, 'Bats': 200, 'Skeletons': 50, 'Cave Insects': 125, 'Duggies': 30, 'Dust Sprites': 500}))
    put(e['meta'], 'categories', table(13))
    put(e['meta'], 'monsters', table(14))
    if truth(binary('>=', call(e['compareSemVer'], get(e['saveInfo'], 'version'), '1.4'), 0)):
        put(get(e['meta'], 'goals'), 'Rock Crabs', 60)
        put(get(e['meta'], 'goals'), 'Mummies', 100)
        put(get(e['meta'], 'goals'), 'Pepper Rex', 50)
        put(get(e['meta'], 'goals'), 'Serpents', 250)
        put(get(e['meta'], 'categories'), 'Rock Crab', 'Rock Crabs')
        put(get(e['meta'], 'categories'), 'Lava Crab', 'Rock Crabs')
        put(get(e['meta'], 'categories'), 'Iridium Crab', 'Rock Crabs')
        put(get(e['meta'], 'categories'), 'Mummy', 'Mummies')
        put(get(e['meta'], 'categories'), 'Pepper Rex', 'Pepper Rex')
        put(get(e['meta'], 'categories'), 'Serpent', 'Serpents')
        put(get(e['meta'], 'monsters'), 'Rock Crabs', Array(['Rock Crab', 'Lava Crab', 'Iridium Crab']))
        put(get(e['meta'], 'monsters'), 'Mummies', Array(['Mummy']))
        put(get(e['meta'], 'monsters'), 'Pepper Rex', Array(['Pepper Rex']))
        put(get(e['meta'], 'monsters'), 'Serpents', Array(['Serpent']))
    if truth(binary('>=', call(e['compareSemVer'], get(e['saveInfo'], 'version'), '1.5'), 0)):
        put(get(e['meta'], 'goals'), 'Flame Spirits', 150)
        put(get(e['meta'], 'categories'), 'Magma Sprite', 'Flame Spirits')
        put(get(e['meta'], 'categories'), 'Magma Sparker', 'Flame Spirits')
        put(get(e['meta'], 'monsters'), 'Flame Spirits', Array(['Magma Sprite', 'Magma Sparker']))
        put(get(e['meta'], 'categories'), 'Tiger Slime', 'Slimes')
        call(get(get(get(e['meta'], 'monsters'), 'Slimes'), 'push'), 'Tiger Slime')
        put(get(e['meta'], 'categories'), 'Shadow Sniper', 'Void Spirits')
        call(get(get(get(e['meta'], 'monsters'), 'Void Spirits'), 'push'), 'Shadow Sniper')
        put(get(e['meta'], 'categories'), 'Magma Duggy', 'Duggies')
        call(get(get(get(e['meta'], 'monsters'), 'Duggies'), 'push'), 'Magma Duggy')
        put(get(e['meta'], 'categories'), 'Iridium Bat', 'Bats')
        call(get(get(get(e['meta'], 'monsters'), 'Bats'), 'push'), 'Iridium Bat')
        put(get(e['meta'], 'categories'), 'Royal Serpent', 'Serpents')
        call(get(get(get(e['meta'], 'monsters'), 'Serpents'), 'push'), 'Royal Serpent')
        call(get(get(get(e['meta'], 'monsters'), 'Skeletons'), 'push'), 'Skeleton Mage')
    if truth(binary('>=', call(e['compareSemVer'], get(e['saveInfo'], 'version'), '1.6'), 0)):
        put(get(e['meta'], 'goals'), 'Cave Insects', 80)
    put(e['table'], 0, call(e['parsePlayerMonsters'], call(get(call(e['$'], e['xmlDoc']), 'find'), 'SaveGame > player'), e['saveInfo'], e['meta']))
    call(e['parseFarmhands'], e['xmlDoc'], e['saveInfo'], e['table'], e['parsePlayerMonsters'], e['meta'])
    e.set('playerOutput', binary('+', e['playerOutput'], call(e['printTranspose'], e['table'])))
    e.set('output', binary('+', binary('+', call(e['getSectionHeader'], e['saveInfo'], e['title'], e['anchor'], get(e['meta'], 'hasDetails'), e['version']), e['playerOutput']), call(e['getSectionFooter'])))
    return e['output']
    return U


def callback_140(parent, this, args):
    # Upstream checkup: 3298
    e = Env(parent)
    e.declare(['id', 'num', 'old'])
    e.local['arguments'] = Array(args)
    e.set('id', call(get(call(get(call(e['$'], this), 'find'), 'key > string'), 'text')))
    e.set('num', call(e['Number'], call(get(call(get(call(e['$'], this), 'find'), 'value > int'), 'text'))))
    e.set('old', 0)
    if truth((binary('>', e['num'], 0) if truth(_logic141 := call(get(get(e['meta'], 'categories'), 'hasOwnProperty'), e['id'])) else _logic141)):
        if truth(call(get(e['killed'], 'hasOwnProperty'), get(get(e['meta'], 'categories'), e['id']))):
            e.set('old', get(e['killed'], get(get(e['meta'], 'categories'), e['id'])))
        put(e['killed'], get(get(e['meta'], 'categories'), e['id']), binary('+', e['old'], e['num']))
    return U


def parsePlayerMonsters_139(parent, this, args):
    # Upstream checkup: 3243
    e = Env(parent)
    e.declare(['completed', 'farmer', 'goal_count', 'hasSkullKey', 'id', 'killed', 'mineLevel', 'need', 'output', 'pt_pct', 'stats', 'table', 'totalMonstersKilled', 'umid'])
    e.local['arguments'] = Array(args)
    e.local['player'] = (args[0] if len(args) > 0 and args[0] is not U else U)
    e.local['saveInfo'] = (args[1] if len(args) > 1 and args[1] is not U else U)
    e.local['meta'] = (args[2] if len(args) > 2 and args[2] is not U else U)
    e.set('output', '')
    e.set('table', Array([]))
    e.set('goal_count', get(call(get(e['Object'], 'keys'), get(e['meta'], 'goals')), 'length'))
    e.set('killed', Array([]))
    e.set('completed', 0)
    e.set('need', Array([]))
    e.set('umid', (call(get(call(get(call(e['$'], e['player']), 'children'), 'UniqueMultiplayerID'), 'text')) if truth(binary('>=', call(e['compareSemVer'], get(e['saveInfo'], 'version'), '1.3'), 0)) else get(e['saveInfo'], 'farmerId')))
    e.set('pt_pct', '')
    e.set('mineLevel', call(e['Number'], call(get(call(get(call(e['$'], e['player']), 'children'), 'deepestMineLevel'), 'text'))))
    e.set('hasSkullKey', call(get(call(get(call(e['$'], e['player']), 'children'), 'hasSkullKey'), 'text')))
    e.set('farmer', call(get(call(get(call(e['$'], e['player']), 'children'), 'name'), 'html')))
    if truth(binary('===', e['hasSkullKey'], 'true')):
        e.set('mineLevel', call(get(e['Math'], 'max'), 120, e['mineLevel']))
    e.set('output', binary('+', e['output'], binary('+', binary('+', binary('+', binary('+', '<div class="', get(e['meta'], 'anchor')), '_summary '), get(e['meta'], 'sum_class')), '">')))
    if truth(binary('<=', e['mineLevel'], 0)):
        e.set('output', binary('+', e['output'], binary('+', binary('+', '<span class="result">', e['farmer']), ' has not yet explored the mines.</span><br />\n')))
    else:
        e.set('output', binary('+', e['output'], binary('+', binary('+', binary('+', binary('+', '<span class="result">', e['farmer']), ' has reached level '), call(get(e['Math'], 'min'), e['mineLevel'], 120)), ' of the mines.</span><br />\n')))
        e.set('output', binary('+', e['output'], binary('+', binary('+', '<span class="result">', e['farmer']), (binary('+', binary('+', ' has reached level ', binary('-', e['mineLevel'], 120)), ' of the Skull Cavern') if truth(binary('>', e['mineLevel'], 120)) else ' has not yet explored the Skull Cavern'))))
        e.set('output', binary('+', e['output'], '.</span></div>'))
    e.set('output', binary('+', e['output'], binary('+', binary('+', binary('+', binary('+', '<div class="', get(e['meta'], 'anchor')), '_summary '), get(e['meta'], 'sum_class')), '">')))
    e.set('output', binary('+', e['output'], '<ul class="ach_list"><li>\n'))
    e.set('output', binary('+', e['output'], (call(e['getAchieveString'], 'The Bottom', 'reach mine level 120', 1) if truth(binary('>=', e['mineLevel'], 120)) else binary('+', binary('+', call(e['getAchieveString'], 'The Bottom', 'reach mine level 120', 0), binary('-', 120, e['mineLevel'])), ' more'))))
    e.set('output', binary('+', e['output'], '</li></ul></div>'))
    if truth(binary('>=', call(e['compareSemVer'], get(e['saveInfo'], 'version'), '1.6'), 0)):
        e.set('totalMonstersKilled', (call(e['Number'], get(get(get(get(e['saveInfo'], 'data'), e['umid']), 'stats'), 'monstersKilled')) if truth(call(get(get(get(get(e['saveInfo'], 'data'), e['umid']), 'stats'), 'hasOwnProperty'), 'monstersKilled')) else 0))
        e.set('output', binary('+', e['output'], binary('+', binary('+', binary('+', binary('+', '<div class="', get(e['meta'], 'anchor')), '_summary '), get(e['meta'], 'sum_class')), '">')))
        e.set('output', binary('+', e['output'], binary('+', binary('+', binary('+', binary('+', '<span class="result">', e['farmer']), ' has killed '), call(e['addCommas'], e['totalMonstersKilled'])), ' monsters</span><br />\n')))
        e.set('output', binary('+', e['output'], '<ul class="ach_list"><li>\n'))
        e.set('output', binary('+', e['output'], (call(e['getMilestoneString'], 'Gain access to the Adventure Guild back room', 1) if truth(binary('>=', e['totalMonstersKilled'], 1000)) else binary('+', binary('+', binary('+', call(e['getMilestoneString'], 'Gain access to the Adventure Guild back room', 0), ' to kill '), binary('-', 1000, e['totalMonstersKilled'])), ' more monsters'))))
        e.set('output', binary('+', e['output'], '</li></ul></div>'))
    if truth(binary('>=', call(e['compareSemVer'], get(e['saveInfo'], 'version'), '1.3'), 0)):
        e.set('stats', call(get(call(e['$'], e['player']), 'find'), 'stats > specificMonstersKilled'))
    else:
        e.set('stats', call(get(call(get(call(e['$'], e['player']), 'parent')), 'find'), 'stats > specificMonstersKilled'))
    call(get(call(get(call(e['$'], e['stats']), 'children'), 'item'), 'each'), Fn(callback_140, e))
    for _key142 in keys(get(e['meta'], 'goals')):
        e.set('id', _key142)
        if truth(call(get(get(e['meta'], 'goals'), 'hasOwnProperty'), e['id'])):
            if truth(call(get(e['killed'], 'hasOwnProperty'), e['id'])):
                if truth(binary('>=', get(e['killed'], e['id']), get(get(e['meta'], 'goals'), e['id']))):
                    update_env(e, 'completed', 1, False)
                else:
                    call(get(e['need'], 'push'), binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', '<li>', e['id']), ' -- kill '), binary('-', get(get(e['meta'], 'goals'), e['id']), get(e['killed'], e['id']))), ' more of: '), call(get(call(get(get(get(e['meta'], 'monsters'), e['id']), 'map'), e['wikimap']), 'join'), ', ')), '</li>'))
            else:
                call(get(e['need'], 'push'), binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', '<li>', e['id']), ' -- kill '), get(get(e['meta'], 'goals'), e['id'])), ' more of: '), call(get(call(get(get(get(e['meta'], 'monsters'), e['id']), 'map'), e['wikimap']), 'join'), ', ')), '</li>'))
    if truth(binary('>=', call(e['compareSemVer'], get(e['saveInfo'], 'version'), '1.5'), 0)):
        put(get(get(e['saveInfo'], 'perfectionTracker'), e['umid']), 'Monsters', binary('>=', e['completed'], e['goal_count']))
        e.set('pt_pct', call(e['getPTLink'], ('Yes' if truth(binary('>=', e['completed'], e['goal_count'])) else 'No')))
    e.set('output', binary('+', e['output'], binary('+', binary('+', binary('+', binary('+', '<div class="', get(e['meta'], 'anchor')), '_summary '), get(e['meta'], 'sum_class')), '">')))
    e.set('output', binary('+', e['output'], binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', '<span class="result">', e['farmer']), ' has completed '), e['completed']), ' of the '), e['goal_count']), ' Monster Eradication goals.'), e['pt_pct']), '</span><ul class="ach_list">\n')))
    e.set('output', binary('+', e['output'], '<li>'))
    e.set('output', binary('+', e['output'], (call(e['getAchieveString'], 'Protector of the Valley', 'all monster goals', 1) if truth(binary('>=', e['completed'], e['goal_count'])) else binary('+', binary('+', call(e['getAchieveString'], 'Protector of the Valley', 'all monster goals', 0), binary('-', e['goal_count'], e['completed'])), ' more'))))
    e.set('output', binary('+', e['output'], '</li></ul></div>'))
    if truth(binary('>', get(e['need'], 'length'), 0)):
        put(e['meta'], 'hasDetails', True)
        e.set('output', binary('+', e['output'], binary('+', binary('+', binary('+', binary('+', '<div class="', get(e['meta'], 'anchor')), '_details '), get(e['meta'], 'det_class')), '">')))
        e.set('output', binary('+', e['output'], binary('+', binary('+', '<span class="need">Goals left:<ol>', call(get(call(get(e['need'], 'sort')), 'join'), '')), '</ol></span></div>')))
    call(get(e['table'], 'push'), e['output'])
    return e['table']
    return U


def parseQuests_143(parent, this, args):
    # Upstream checkup: 3345
    e = Env(parent)
    e.declare(['anchor', 'det_class', 'meta', 'output', 'playerOutput', 'sum_class', 'table', 'title', 'version'])
    e.local['arguments'] = Array(args)
    e.local['xmlDoc'] = (args[0] if len(args) > 0 and args[0] is not U else U)
    e.local['saveInfo'] = (args[1] if len(args) > 1 and args[1] is not U else U)
    e.set('title', 'Quests')
    e.set('anchor', call(e['makeAnchor'], e['title']))
    e.set('version', '1.2')
    e.set('sum_class', call(e['getSummaryClass'], e['saveInfo'], e['version']))
    e.set('det_class', call(e['getDetailsClass'], e['saveInfo'], e['version']))
    e.set('output', '')
    e.set('playerOutput', '')
    e.set('meta', Obj({'hasDetails': False, 'anchor': e['anchor'], 'sum_class': e['sum_class'], 'det_class': e['det_class']}))
    e.set('table', Array([]))
    put(e['table'], 0, call(e['parsePlayerQuests'], call(get(call(e['$'], e['xmlDoc']), 'find'), 'SaveGame > player'), e['saveInfo'], e['meta']))
    call(e['parseFarmhands'], e['xmlDoc'], e['saveInfo'], e['table'], e['parsePlayerQuests'], e['meta'])
    e.set('playerOutput', binary('+', e['playerOutput'], call(e['printTranspose'], e['table'])))
    e.set('output', binary('+', binary('+', call(e['getSectionHeader'], e['saveInfo'], e['title'], e['anchor'], get(e['meta'], 'hasDetails'), e['version']), e['playerOutput']), call(e['getSectionFooter'])))
    return e['output']
    return U


def parsePlayerQuests_144(parent, this, args):
    # Upstream checkup: 3363
    e = Env(parent)
    e.declare(['count', 'output'])
    e.local['arguments'] = Array(args)
    e.local['player'] = (args[0] if len(args) > 0 and args[0] is not U else U)
    e.local['saveInfo'] = (args[1] if len(args) > 1 and args[1] is not U else U)
    e.local['meta'] = (args[2] if len(args) > 2 and args[2] is not U else U)
    e.set('output', '')
    if truth(binary('>=', call(e['compareSemVer'], get(e['saveInfo'], 'version'), '1.6'), 0)):
        e.set('count', call(e['Number'], call(get(call(get(call(e['$'], e['player']), 'find'), 'stats > Values > item:contains("questsCompleted") > value > *'), 'text'))))
    else:
        if truth(binary('>=', call(e['compareSemVer'], get(e['saveInfo'], 'version'), '1.3'), 0)):
            e.set('count', call(e['Number'], call(get(call(get(call(e['$'], e['player']), 'find'), 'stats > questsCompleted'), 'text'))))
        else:
            e.set('count', call(e['Number'], call(get(call(get(call(get(call(e['$'], e['player']), 'parent')), 'find'), 'stats > questsCompleted'), 'text'))))
    e.set('output', binary('+', e['output'], binary('+', binary('+', binary('+', binary('+', '<div class="', get(e['meta'], 'anchor')), '_summary '), get(e['meta'], 'sum_class')), '">')))
    e.set('output', binary('+', e['output'], binary('+', binary('+', binary('+', binary('+', '<span class="result">', call(get(call(get(call(e['$'], e['player']), 'children'), 'name'), 'html'))), ' has completed '), e['count']), ' "Help Wanted" quest(s).</span><br />\n')))
    e.set('output', binary('+', e['output'], '<ul class="ach_list"><li>'))
    e.set('output', binary('+', e['output'], (call(e['getAchieveString'], 'Gofer', 'complete 10 quests', 1) if truth(binary('>=', e['count'], 10)) else binary('+', binary('+', call(e['getAchieveString'], 'Gofer', 'complete 10 quests', 0), binary('-', 10, e['count'])), ' more'))))
    e.set('output', binary('+', e['output'], '</li>\n<li>'))
    e.set('output', binary('+', e['output'], (call(e['getAchieveString'], 'A Big Help', 'complete 40 quests', 1) if truth(binary('>=', e['count'], 40)) else binary('+', binary('+', call(e['getAchieveString'], 'A Big Help', 'complete 40 quests', 0), binary('-', 40, e['count'])), ' more'))))
    e.set('output', binary('+', e['output'], '</li></ul></div>'))
    return Array([e['output']])
    return U


def parseStardrops_145(parent, this, args):
    # Upstream checkup: 3388
    e = Env(parent)
    e.declare(['anchor', 'det_class', 'meta', 'output', 'playerOutput', 'sum_class', 'table', 'title', 'version'])
    e.local['arguments'] = Array(args)
    e.local['xmlDoc'] = (args[0] if len(args) > 0 and args[0] is not U else U)
    e.local['saveInfo'] = (args[1] if len(args) > 1 and args[1] is not U else U)
    e.set('title', 'Stardrops')
    e.set('anchor', call(e['makeAnchor'], e['title']))
    e.set('version', '1.2')
    e.set('sum_class', call(e['getSummaryClass'], e['saveInfo'], e['version']))
    e.set('det_class', call(e['getDetailsClass'], e['saveInfo'], e['version']))
    e.set('output', '')
    e.set('playerOutput', '')
    e.set('meta', Obj({'hasDetails': False, 'anchor': e['anchor'], 'sum_class': e['sum_class'], 'det_class': e['det_class']}))
    e.set('table', Array([]))
    put(e['meta'], 'stardrops', table(15))
    put(e['table'], 0, call(e['parsePlayerStardrops'], call(get(call(e['$'], e['xmlDoc']), 'find'), 'SaveGame > player'), e['saveInfo'], e['meta']))
    call(e['parseFarmhands'], e['xmlDoc'], e['saveInfo'], e['table'], e['parsePlayerStardrops'], e['meta'])
    e.set('playerOutput', binary('+', e['playerOutput'], call(e['printTranspose'], e['table'])))
    e.set('output', binary('+', binary('+', call(e['getSectionHeader'], e['saveInfo'], e['title'], e['anchor'], get(e['meta'], 'hasDetails'), e['version']), e['playerOutput']), call(e['getSectionFooter'])))
    return e['output']
    return U


def parsePlayerStardrops_146(parent, this, args):
    # Upstream checkup: 3417
    e = Env(parent)
    e.declare(['altTrigger', 'count', 'id', 'need', 'output', 'pt_pct', 'staminaOverride', 'stardrop_count', 'umid'])
    e.local['arguments'] = Array(args)
    e.local['player'] = (args[0] if len(args) > 0 and args[0] is not U else U)
    e.local['saveInfo'] = (args[1] if len(args) > 1 and args[1] is not U else U)
    e.local['meta'] = (args[2] if len(args) > 2 and args[2] is not U else U)
    e.set('output', '')
    e.set('count', 0)
    e.set('umid', (call(get(call(get(call(e['$'], e['player']), 'children'), 'UniqueMultiplayerID'), 'text')) if truth(binary('>=', call(e['compareSemVer'], get(e['saveInfo'], 'version'), '1.3'), 0)) else get(e['saveInfo'], 'farmerId')))
    e.set('pt_pct', '')
    e.set('need', Array([]))
    e.set('staminaOverride', False)
    e.set('stardrop_count', get(call(get(e['Object'], 'keys'), get(e['meta'], 'stardrops')), 'length'))
    for _key147 in keys(get(e['meta'], 'stardrops')):
        e.set('id', _key147)
        if truth(call(get(get(e['meta'], 'stardrops'), 'hasOwnProperty'), e['id'])):
            e.set('altTrigger', (binary('===', get(get(get(get(e['saveInfo'], 'data'), e['umid']), 'chestConsumedMineLevels'), 100), 'true') if truth(_logic148 := (call(get(get(get(get(e['saveInfo'], 'data'), e['umid']), 'chestConsumedMineLevels'), 'hasOwnProperty'), 100) if truth(_logic149 := binary('==', e['id'], 'CF_Mines')) else _logic149)) else _logic148))
            if truth((_logic150 if truth(_logic150 := call(get(get(get(get(e['saveInfo'], 'data'), e['umid']), 'mailReceived'), 'hasOwnProperty'), e['id'])) else e['altTrigger'])):
                update_env(e, 'count', 1, False)
            else:
                call(get(e['need'], 'push'), binary('+', binary('+', '<li>', get(get(e['meta'], 'stardrops'), e['id'])), '</li>'))
    if truth(call(get(get(get(get(e['saveInfo'], 'data'), e['umid']), 'mailReceived'), 'hasOwnProperty'), 'gotMaxStamina')):
        e.set('staminaOverride', True)
    if truth(binary('>=', call(e['compareSemVer'], get(e['saveInfo'], 'version'), '1.5'), 0)):
        put(get(get(e['saveInfo'], 'perfectionTracker'), e['umid']), 'Stardrops', binary('>=', e['count'], e['stardrop_count']))
        e.set('pt_pct', call(e['getPTLink'], ('Yes' if truth((_logic151 if truth(_logic151 := e['staminaOverride']) else binary('>=', e['count'], e['stardrop_count']))) else 'No')))
    e.set('output', binary('+', e['output'], binary('+', binary('+', binary('+', binary('+', '<div class="', get(e['meta'], 'anchor')), '_summary '), get(e['meta'], 'sum_class')), '">')))
    e.set('output', binary('+', e['output'], binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', '<span class="result">', get(get(e['saveInfo'], 'players'), e['umid'])), ' has '), ('' if truth(e['staminaOverride']) else 'not ')), ' reached 508 max stamina (actual amount '), get(get(get(e['saveInfo'], 'data'), e['umid']), 'maxStamina')), ')</span><br/>')))
    if truth((binary('<', e['count'], e['stardrop_count']) if truth(_logic152 := e['staminaOverride']) else _logic152)):
        e.set('output', binary('+', e['output'], '<span class="result note">Note: Stamina will override stardrop marker count for achievements and perfection.</span><br/>'))
    e.set('output', binary('+', e['output'], binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', '<span class="result">', get(get(e['saveInfo'], 'players'), e['umid'])), ' has markers for '), e['count']), ' of '), e['stardrop_count']), ' stardrops.'), e['pt_pct']), '</span><br/>')))
    e.set('output', binary('+', e['output'], '<ul class="ach_list"><li>'))
    e.set('output', binary('+', e['output'], (call(e['getAchieveString'], 'Mystery Of The Stardrops', 'find every stardrop', 1) if truth(binary('>=', e['count'], e['stardrop_count'])) else binary('+', binary('+', call(e['getAchieveString'], 'Mystery Of The Stardrops', 'find every stardrop', 0), binary('-', e['stardrop_count'], e['count'])), ' more'))))
    e.set('output', binary('+', e['output'], '</li></ul></div>'))
    if truth(binary('>', get(e['need'], 'length'), 0)):
        put(e['meta'], 'hasDetails', True)
        e.set('output', binary('+', e['output'], binary('+', binary('+', binary('+', binary('+', '<div class="', get(e['meta'], 'anchor')), '_details '), get(e['meta'], 'det_class')), '">')))
        e.set('output', binary('+', e['output'], binary('+', binary('+', '<span class="need">Stardrops left:<ol>', call(get(call(get(e['need'], 'sort')), 'join'), '')), '</ol></span></div>')))
    return Array([e['output']])
    return U


def callback_154(parent, this, args):
    # Upstream checkup: 3544
    e = Env(parent)
    e.declare(['id'])
    e.local['arguments'] = Array(args)
    e.set('id', call(get(call(e['$'], this), 'text')))
    if truth(call(get(e['achieves'], 'hasOwnProperty'), e['id'])):
        update_env(e, 'count', 1, False)
        put(e['ach_have'], e['id'], 1)
    return U


def callback_158(parent, this, args):
    # Upstream checkup: 3587
    e = Env(parent)
    e.declare(['num'])
    e.local['arguments'] = Array(args)
    e.set('num', call(e['Number'], call(get(call(get(call(e['$'], this), 'find'), 'value > Friendship > Points'), 'text'))))
    if truth(binary('>=', e['num'], 1975)):
        update_env(e, 'heart_count', 1, False)
    return U


def callback_159(parent, this, args):
    # Upstream checkup: 3592
    e = Env(parent)
    e.declare(['num'])
    e.local['arguments'] = Array(args)
    e.set('num', call(e['Number'], call(get(call(get(call(get(call(e['$'], this), 'find'), 'value > ArrayOfInt > int'), 'first')), 'text'))))
    if truth(binary('>=', e['num'], 1975)):
        update_env(e, 'heart_count', 1, False)
    return U


def callback_160(parent, this, args):
    # Upstream checkup: 3607
    e = Env(parent)
    e.declare(['thisPetLove'])
    e.local['arguments'] = Array(args)
    if truth((_logic161 if truth(_logic161 := (_logic162 if truth(_logic162 := binary('===', call(get(call(e['$'], this), 'attr'), binary('+', get(e['saveInfo'], 'ns_prefix'), ':type')), 'Pet')) else binary('===', call(get(call(e['$'], this), 'attr'), binary('+', get(e['saveInfo'], 'ns_prefix'), ':type')), 'Cat'))) else binary('===', call(get(call(e['$'], this), 'attr'), binary('+', get(e['saveInfo'], 'ns_prefix'), ':type')), 'Dog'))):
        e.set('hasPet', 1)
        e.set('thisPetLove', call(e['Number'], call(get(call(get(call(e['$'], this), 'find'), 'friendshipTowardFarmer'), 'text'))))
        if truth(binary('>', e['thisPetLove'], e['petLove'])):
            e.set('petLove', e['thisPetLove'])
    return U


def parseGrandpa_153(parent, this, args):
    # Upstream checkup: 3466
    e = Env(parent)
    e.declare(['ach_count', 'ach_have', 'achieves', 'anchor', 'candles', 'ccRooms', 'cc_count', 'cc_done', 'cc_have', 'count', 'currentCandles', 'det_class', 'farmer', 'hasKeys', 'hasPet', 'hasRustyKey', 'hasSkullKey', 'heart_count', 'houseUpgrades', 'id', 'isJojaMember', 'max_candles', 'max_count', 'money', 'need', 'output', 'petLove', 'playerLevel', 'realPlayerLevel', 'spouse', 'sum_class', 'title', 'uid', 'version'])
    e.local['arguments'] = Array(args)
    e.local['xmlDoc'] = (args[0] if len(args) > 0 and args[0] is not U else U)
    e.local['saveInfo'] = (args[1] if len(args) > 1 and args[1] is not U else U)
    e.set('title', "Grandpa's Evaluation")
    e.set('anchor', call(e['makeAnchor'], e['title']))
    e.set('version', '1.2')
    e.set('sum_class', call(e['getSummaryClass'], e['saveInfo'], e['version']))
    e.set('det_class', call(e['getDetailsClass'], e['saveInfo'], e['version']))
    e.set('output', '')
    e.set('farmer', call(get(call(get(call(e['$'], e['xmlDoc']), 'find'), 'player > name'), 'html')))
    e.set('count', 0)
    e.set('max_count', 21)
    e.set('candles', 1)
    e.set('max_candles', 4)
    e.set('currentCandles', call(e['Number'], call(get(call(get(call(e['$'], e['xmlDoc']), 'find'), binary('+', binary('+', 'locations > GameLocation[', get(e['saveInfo'], 'ns_prefix')), "\\:type='Farm'] > grandpaScore")), 'text'))))
    e.set('need', '')
    e.set('money', call(e['Number'], call(get(call(get(call(e['$'], e['xmlDoc']), 'find'), 'player > totalMoneyEarned'), 'text'))))
    e.set('achieves', Obj({'5': 'A Complete Collection', '26': 'Master Angler', '34': 'Full Shipment'}))
    e.set('ach_count', 3)
    e.set('ach_have', Obj({}))
    e.set('cc_done', 0)
    e.set('ccRooms', table(16))
    e.set('cc_have', 0)
    e.set('cc_count', 6)
    e.set('isJojaMember', 0)
    e.set('spouse', call(get(call(e['$'], e['xmlDoc']), 'find'), 'player > spouse'))
    e.set('houseUpgrades', call(e['Number'], call(get(call(get(call(e['$'], e['xmlDoc']), 'find'), 'player > houseUpgradeLevel'), 'text'))))
    e.set('hasRustyKey', 'false')
    e.set('hasSkullKey', 'false')
    e.set('hasKeys', Array([]))
    e.set('heart_count', 0)
    e.set('hasPet', 0)
    e.set('petLove', 0)
    e.set('realPlayerLevel', binary('+', binary('+', binary('+', binary('+', binary('+', call(e['Number'], call(get(call(get(call(e['$'], e['xmlDoc']), 'find'), 'player > farmingLevel'), 'text'))), call(e['Number'], call(get(call(get(call(e['$'], e['xmlDoc']), 'find'), 'player > miningLevel'), 'text')))), call(e['Number'], call(get(call(get(call(e['$'], e['xmlDoc']), 'find'), 'player > combatLevel'), 'text')))), call(e['Number'], call(get(call(get(call(e['$'], e['xmlDoc']), 'find'), 'player > foragingLevel'), 'text')))), call(e['Number'], call(get(call(get(call(e['$'], e['xmlDoc']), 'find'), 'player > fishingLevel'), 'text')))), call(e['Number'], call(get(call(get(call(e['$'], e['xmlDoc']), 'find'), 'player > luckLevel'), 'text')))))
    e.set('playerLevel', binary('/', e['realPlayerLevel'], 2))
    if truth(binary('>=', call(e['compareSemVer'], get(e['saveInfo'], 'version'), '1.6'), 0)):
        if truth(call(get(get(get(get(e['saveInfo'], 'data'), get(e['saveInfo'], 'farmerId')), 'mailReceived'), 'hasOwnProperty'), 'HasRustyKey')):
            e.set('hasRustyKey', 'true')
        if truth(call(get(get(get(get(e['saveInfo'], 'data'), get(e['saveInfo'], 'farmerId')), 'mailReceived'), 'hasOwnProperty'), 'HasSkullKey')):
            e.set('hasSkullKey', 'true')
    else:
        e.set('hasRustyKey', call(get(call(get(call(e['$'], e['xmlDoc']), 'find'), 'player > hasRustyKey'), 'text')))
        e.set('hasSkullKey', call(get(call(get(call(e['$'], e['xmlDoc']), 'find'), 'player > hasSkullKey'), 'text')))
    if truth(binary('>=', e['money'], 1000000)):
        e.set('count', binary('+', e['count'], 7))
    else:
        if truth(binary('>=', e['money'], 500000)):
            e.set('count', binary('+', e['count'], 5))
        else:
            if truth(binary('>=', e['money'], 300000)):
                e.set('count', binary('+', e['count'], 4))
            else:
                if truth(binary('>=', e['money'], 200000)):
                    e.set('count', binary('+', e['count'], 3))
                else:
                    if truth(binary('>=', e['money'], 100000)):
                        e.set('count', binary('+', e['count'], 2))
                    else:
                        if truth(binary('>=', e['money'], 50000)):
                            e.set('count', binary('+', e['count'], 1))
    call(get(call(get(call(e['$'], e['xmlDoc']), 'find'), 'player > achievements > int'), 'each'), Fn(callback_154, e))
    if truth(call(get(get(get(get(e['saveInfo'], 'data'), get(e['saveInfo'], 'farmerId')), 'eventsSeen'), 'hasOwnProperty'), '191393')):
        e.set('cc_done', 1)
    if truth(e['cc_done']):
        e.set('count', binary('+', e['count'], 3))
    else:
        if truth(call(get(get(get(get(e['saveInfo'], 'data'), get(e['saveInfo'], 'farmerId')), 'mailReceived'), 'hasOwnProperty'), 'JojaMember')):
            e.set('isJojaMember', 1)
        for _key155 in keys(e['ccRooms']):
            e.set('id', _key155)
            if truth((call(get(get(get(get(e['saveInfo'], 'data'), get(e['saveInfo'], 'farmerId')), 'mailReceived'), 'hasOwnProperty'), e['id']) if truth(_logic156 := call(get(e['ccRooms'], 'hasOwnProperty'), e['id'])) else _logic156)):
                update_env(e, 'cc_have', 1, False)
        if truth(binary('>=', e['cc_have'], e['cc_count'])):
            update_env(e, 'count', 1, False)
    if truth(binary('===', e['hasRustyKey'], 'true')):
        update_env(e, 'count', 1, False)
        call(get(e['hasKeys'], 'push'), 'Rusty Key')
    if truth(binary('===', e['hasSkullKey'], 'true')):
        update_env(e, 'count', 1, False)
        call(get(e['hasKeys'], 'push'), 'Skull Key')
    if truth(binary('>=', call(e['compareSemVer'], get(e['saveInfo'], 'version'), '1.3'), 0)):
        e.set('uid', call(get(call(get(call(get(call(e['$'], e['xmlDoc']), 'find'), 'player'), 'children'), 'UniqueMultiplayerID'), 'text')))
        if truth(call(get(get(e['saveInfo'], 'partners'), 'hasOwnProperty'), e['uid'])):
            e.set('spouse', get(get(e['saveInfo'], 'players'), get(get(e['saveInfo'], 'partners'), e['uid'])))
    if truth((binary('>=', e['houseUpgrades'], 2) if truth(_logic157 := binary('>', get(e['spouse'], 'length'), 0)) else _logic157)):
        update_env(e, 'count', 1, False)
    if truth(binary('>=', call(e['compareSemVer'], get(e['saveInfo'], 'version'), '1.3'), 0)):
        call(get(call(get(call(e['$'], e['xmlDoc']), 'find'), 'player> friendshipData > item'), 'each'), Fn(callback_158, e))
    else:
        call(get(call(get(call(e['$'], e['xmlDoc']), 'find'), 'player> friendships > item'), 'each'), Fn(callback_159, e))
    if truth(binary('>=', e['heart_count'], 10)):
        e.set('count', binary('+', e['count'], 2))
    else:
        if truth(binary('>=', e['heart_count'], 5)):
            e.set('count', binary('+', e['count'], 1))
    if truth(binary('>=', e['playerLevel'], 25)):
        e.set('count', binary('+', e['count'], 2))
    else:
        if truth(binary('>=', e['playerLevel'], 15)):
            e.set('count', binary('+', e['count'], 1))
    call(get(call(get(call(e['$'], e['xmlDoc']), 'find'), 'locations > GameLocation > Characters > NPC'), 'each'), Fn(callback_160, e))
    if truth(binary('>=', call(e['compareSemVer'], get(e['saveInfo'], 'version'), '1.6'), 0)):
        if truth(call(get(get(get(get(e['saveInfo'], 'data'), get(e['saveInfo'], 'farmerId')), 'mailReceived'), 'hasOwnProperty'), 'petLoveMessage')):
            e.set('petLove', 1000)
    if truth(binary('>=', e['petLove'], 999)):
        update_env(e, 'count', 1, False)
    if truth(binary('>=', e['count'], 12)):
        e.set('candles', 4)
    else:
        if truth(binary('>=', e['count'], 8)):
            e.set('candles', 3)
        else:
            if truth(binary('>=', e['count'], 4)):
                e.set('candles', 2)
    e.set('output', call(e['getSectionHeader'], e['saveInfo'], e['title'], e['anchor'], True, e['version']))
    e.set('output', binary('+', e['output'], binary('+', binary('+', binary('+', binary('+', '<div class="', e['anchor']), '_summary '), e['sum_class']), '">')))
    e.set('output', binary('+', e['output'], binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', '<span class="result">', e['farmer']), ' has earned a total of '), e['count']), ' point(s) (details below); the maximum possible is '), e['max_count']), ' points.</span><br />\n')))
    e.set('output', binary('+', e['output'], binary('+', binary('+', binary('+', binary('+', '<span class="result">The shrine has ', e['currentCandles']), ' candle(s) lit. The next evaluation will light '), e['candles']), ' candle(s).</span><br />\n')))
    e.set('output', binary('+', e['output'], '<ul class="ach_list"><li>'))
    e.set('output', binary('+', e['output'], (call(e['getMilestoneString'], 'Four candle evaluation', 1) if truth(binary('>=', e['candles'], e['max_candles'])) else binary('+', binary('+', call(e['getMilestoneString'], 'Four candle evaluation', 0), binary('-', 12, e['count'])), ' more point(s)'))))
    e.set('output', binary('+', e['output'], '</li></ul></span>'))
    e.set('output', binary('+', e['output'], binary('+', binary('+', binary('+', binary('+', '<div class="', e['anchor']), '_details '), e['det_class']), '">')))
    e.set('output', binary('+', e['output'], binary('+', binary('+', binary('+', binary('+', '<span class="result">', e['farmer']), ' has earned a total of '), call(e['addCommas'], e['money'])), 'g.</span><br />\n')))
    e.set('output', binary('+', e['output'], '<ul class="ach_list"><li>'))
    e.set('output', binary('+', e['output'], (call(e['getPointString'], 1, 'at least 50,000g earnings', 0, 1) if truth(binary('>=', e['money'], 50000)) else binary('+', binary('+', binary('+', call(e['getPointString'], 1, 'at least 50,000g earnings', 0, 0), ' -- need '), call(e['addCommas'], binary('-', 50000, e['money']))), 'g more'))))
    e.set('output', binary('+', e['output'], '</li>\n<li>'))
    e.set('output', binary('+', e['output'], (call(e['getPointString'], 1, 'at least 100,000g earnings', 1, 1) if truth(binary('>=', e['money'], 100000)) else binary('+', binary('+', binary('+', call(e['getPointString'], 1, 'at least 100,000g earnings', 1, 0), ' -- need '), call(e['addCommas'], binary('-', 100000, e['money']))), 'g more'))))
    e.set('output', binary('+', e['output'], '</li>\n<li>'))
    e.set('output', binary('+', e['output'], (call(e['getPointString'], 1, 'at least 200,000g earnings', 1, 1) if truth(binary('>=', e['money'], 200000)) else binary('+', binary('+', binary('+', call(e['getPointString'], 1, 'at least 200,000g earnings', 1, 0), ' -- need '), call(e['addCommas'], binary('-', 200000, e['money']))), 'g more'))))
    e.set('output', binary('+', e['output'], '</li>\n<li>'))
    e.set('output', binary('+', e['output'], (call(e['getPointString'], 1, 'at least 300,000g earnings', 1, 1) if truth(binary('>=', e['money'], 300000)) else binary('+', binary('+', binary('+', call(e['getPointString'], 1, 'at least 300,000g earnings', 1, 0), ' -- need '), call(e['addCommas'], binary('-', 300000, e['money']))), 'g more'))))
    e.set('output', binary('+', e['output'], '</li>\n<li>'))
    e.set('output', binary('+', e['output'], (call(e['getPointString'], 1, 'at least 500,000g earnings', 1, 1) if truth(binary('>=', e['money'], 500000)) else binary('+', binary('+', binary('+', call(e['getPointString'], 1, 'at least 500,000g earnings', 1, 0), ' -- need '), call(e['addCommas'], binary('-', 500000, e['money']))), 'g more'))))
    e.set('output', binary('+', e['output'], '</li>\n<li>'))
    e.set('output', binary('+', e['output'], (call(e['getPointString'], 2, 'at least 1,000,000g earnings', 1, 1) if truth(binary('>=', e['money'], 1000000)) else binary('+', binary('+', binary('+', call(e['getPointString'], 2, 'at least 1,000,000g earnings', 1, 0), ' -- need '), call(e['addCommas'], binary('-', 1000000, e['money']))), 'g more'))))
    e.set('output', binary('+', e['output'], '</li></ul>\n'))
    e.set('output', binary('+', e['output'], binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', '<span class="result">', e['farmer']), ' has earned '), get(call(get(e['Object'], 'keys'), e['ach_have']), 'length')), ' of the '), e['ach_count']), ' relevant achievements.</span><br />\n')))
    e.set('output', binary('+', e['output'], '<ul class="ach_list"><li>'))
    e.set('output', binary('+', e['output'], (call(e['getPointString'], 1, '<span class="ach">A Complete Collection</span> Achievement', 0, 1) if truth(call(get(e['ach_have'], 'hasOwnProperty'), 5)) else call(e['getPointString'], 1, '<span class="ach">A Complete Collection</span> Achievement', 0, 0))))
    e.set('output', binary('+', e['output'], '</li>\n<li>'))
    e.set('output', binary('+', e['output'], (call(e['getPointString'], 1, '<span class="ach">Master Angler</span> Achievement', 0, 1) if truth(call(get(e['ach_have'], 'hasOwnProperty'), 26)) else call(e['getPointString'], 1, '<span class="ach">Master Angler</span> Achievement', 0, 0))))
    e.set('output', binary('+', e['output'], '</li>\n<li>'))
    e.set('output', binary('+', e['output'], (call(e['getPointString'], 1, '<span class="ach">Full Shipment</span> Achievement', 0, 1) if truth(call(get(e['ach_have'], 'hasOwnProperty'), 34)) else call(e['getPointString'], 1, '<span class="ach">Full Shipment</span> Achievement', 0, 0))))
    e.set('output', binary('+', e['output'], '</li></ul>\n'))
    if truth(e['isJojaMember']):
        e.set('output', binary('+', e['output'], binary('+', binary('+', '<span class="result">', e['farmer']), ' has purchased a Joja membership and cannot restore the Community Center')))
        e.set('output', binary('+', e['output'], '<ul class="ach_list"><li>'))
        e.set('output', binary('+', e['output'], call(e['getPointImpossibleString'], 1, 'complete Community Center')))
        e.set('output', binary('+', e['output'], '</li>\n<li>'))
        e.set('output', binary('+', e['output'], call(e['getPointImpossibleString'], 2, 'attend the Community Center re-opening')))
        e.set('output', binary('+', e['output'], '</li></ul>\n'))
    else:
        if truth((_logic163 if truth(_logic163 := e['cc_done']) else binary('>=', e['cc_have'], e['cc_count']))):
            e.set('output', binary('+', e['output'], binary('+', binary('+', '<span class="result">', e['farmer']), ' has completed the Community Center restoration')))
            e.set('output', binary('+', e['output'], (' and attended the re-opening ceremony.' if truth(e['cc_done']) else ' but has not yet attended the re-opening ceremony.')))
            e.set('output', binary('+', e['output'], '</span><br />\n'))
        else:
            e.set('output', binary('+', e['output'], binary('+', binary('+', '<span class="result">', e['farmer']), ' has not completed the Community Center restoration.')))
        e.set('output', binary('+', e['output'], '<ul class="ach_list"><li>'))
        e.set('output', binary('+', e['output'], (call(e['getPointString'], 1, 'complete Community Center', 0, 1) if truth((_logic164 if truth(_logic164 := e['cc_done']) else binary('>=', e['cc_have'], e['cc_count']))) else call(e['getPointString'], 1, 'complete Community Center', 0, 0))))
        e.set('output', binary('+', e['output'], '</li>\n<li>'))
        e.set('output', binary('+', e['output'], (call(e['getPointString'], 2, 'attend the Community Center re-opening', 0, 1) if truth(e['cc_done']) else call(e['getPointString'], 2, 'attend the Community Center re-opening', 0, 0))))
        e.set('output', binary('+', e['output'], '</li></ul>\n'))
    e.set('output', binary('+', e['output'], binary('+', binary('+', binary('+', binary('+', '<span class="result">', e['farmer']), ' has '), e['realPlayerLevel']), ' total skill levels.</span><br />\n')))
    e.set('output', binary('+', e['output'], '<ul class="ach_list"><li>'))
    e.set('output', binary('+', e['output'], (call(e['getPointString'], 1, '30 total skill levels', 0, 1) if truth(binary('>=', e['playerLevel'], 15)) else binary('+', binary('+', binary('+', call(e['getPointString'], 1, '30 total skill levels', 0, 0), ' -- need '), binary('-', 30, e['realPlayerLevel'])), ' more'))))
    e.set('output', binary('+', e['output'], '</li>\n<li>'))
    e.set('output', binary('+', e['output'], (call(e['getPointString'], 1, '50 total skill levels', 1, 1) if truth(binary('>=', e['playerLevel'], 25)) else binary('+', binary('+', binary('+', call(e['getPointString'], 1, '50 total skill levels', 1, 0), ' -- need '), binary('-', 50, e['realPlayerLevel'])), ' more'))))
    e.set('output', binary('+', e['output'], '</li></ul>\n'))
    e.set('output', binary('+', e['output'], binary('+', binary('+', binary('+', binary('+', '<span class="result">', e['farmer']), ' has '), e['heart_count']), ' relationship(s) of 1975+ friendship points (~8 hearts.)</span><br />\n')))
    e.set('output', binary('+', e['output'], '<ul class="ach_list"><li>'))
    e.set('output', binary('+', e['output'], (call(e['getPointString'], 1, '~8&#x2665; with 5 people', 0, 1) if truth(binary('>=', e['heart_count'], 5)) else binary('+', binary('+', binary('+', call(e['getPointString'], 1, '~8&#x2665; with 5 people', 0, 0), ' -- need '), binary('-', 5, e['heart_count'])), ' more'))))
    e.set('output', binary('+', e['output'], '</li>\n<li>'))
    e.set('output', binary('+', e['output'], (call(e['getPointString'], 1, '~8&#x2665; with 10 people', 1, 1) if truth(binary('>=', e['heart_count'], 10)) else binary('+', binary('+', binary('+', call(e['getPointString'], 1, '~8&#x2665; with 10 people', 1, 0), ' -- need '), binary('-', 10, e['heart_count'])), ' more'))))
    e.set('output', binary('+', e['output'], '</li></ul>\n'))
    if truth(e['hasPet']):
        e.set('output', binary('+', e['output'], binary('+', binary('+', binary('+', binary('+', '<span class="result">', e['farmer']), ' has a pet with '), e['petLove']), ' friendship points.</span><br/>')))
        e.set('need', binary('+', binary('-', 999, e['petLove']), ' more friendship points'))
    else:
        if truth(binary('>', e['petLove'], 0)):
            e.set('output', binary('+', e['output'], binary('+', binary('+', binary('+', binary('+', '<span class="result">', e['farmer']), ' previously had a pet with '), e['petLove']), ' friendship points.</span><br/>')))
        else:
            e.set('output', binary('+', e['output'], binary('+', binary('+', '<span class="result">', e['farmer']), ' has not had a pet with any friendship points.</span><br/>')))
        e.set('need', 'a pet and 999 friendship points')
    e.set('output', binary('+', e['output'], '<ul class="ach_list"><li>'))
    e.set('output', binary('+', e['output'], (call(e['getPointString'], 1, 'pet with at least 999 friendship points', 0, 1) if truth(binary('>=', e['petLove'], 999)) else binary('+', binary('+', call(e['getPointString'], 1, 'pet with at least 999 friendship points', 0, 0), ' -- need '), e['need']))))
    e.set('output', binary('+', e['output'], '</li></ul>\n'))
    e.set('output', binary('+', e['output'], binary('+', binary('+', binary('+', binary('+', binary('+', '<span class="result">', e['farmer']), (' is' if truth(binary('>', get(e['spouse'], 'length'), 0)) else ' is not')), ' married and has upgraded the farmhouse '), e['houseUpgrades']), ' time(s).</span><br />\n')))
    e.set('output', binary('+', e['output'], '<ul class="ach_list"><li>'))
    e.set('need', Array([]))
    if truth(binary('===', get(e['spouse'], 'length'), 0)):
        call(get(e['need'], 'push'), 'a spouse')
    if truth(binary('<', e['houseUpgrades'], 2)):
        call(get(e['need'], 'push'), binary('+', binary('-', 2, e['houseUpgrades']), ' more upgrade(s)'))
    e.set('output', binary('+', e['output'], (call(e['getPointString'], 1, 'married with at least 2 house upgrades', 0, 1) if truth(binary('===', get(e['need'], 'length'), 0)) else binary('+', binary('+', call(e['getPointString'], 1, 'married with at least 2 house upgrades', 0, 0), ' -- need '), call(get(e['need'], 'join'), ' and ')))))
    e.set('output', binary('+', e['output'], '</li></ul>\n'))
    if truth(binary('>', get(e['hasKeys'], 'length'), 0)):
        e.set('output', binary('+', e['output'], binary('+', binary('+', binary('+', binary('+', '<span class="result">', e['farmer']), ' has acquired the '), call(get(e['hasKeys'], 'join'), ' and ')), '.</span><br />\n')))
    else:
        e.set('output', binary('+', e['output'], binary('+', binary('+', '<span class="result">', e['farmer']), ' has not acquired either the Rusty Key or Skull Key.</span><br />\n')))
    e.set('output', binary('+', e['output'], '<ul class="ach_list"><li>'))
    e.set('output', binary('+', e['output'], (call(e['getPointString'], 1, 'has the Rusty Key', 0, 1) if truth(binary('===', e['hasRustyKey'], 'true')) else binary('+', call(e['getPointString'], 1, 'get the Rusty Key', 0, 0), ' -- acquired after 60 museum donations'))))
    e.set('output', binary('+', e['output'], '</li>\n<li>'))
    e.set('output', binary('+', e['output'], (call(e['getPointString'], 1, 'has the Skull Key', 0, 1) if truth(binary('===', e['hasSkullKey'], 'true')) else binary('+', call(e['getPointString'], 1, 'get the Skull Key', 0, 0), ' -- acquired on level 120 of the mines'))))
    e.set('output', binary('+', e['output'], '</li></ul></div>'))
    e.set('output', binary('+', e['output'], call(e['getSectionFooter'])))
    return e['output']
    return U


def parseBundleData_165(parent, this, args):
    # Upstream checkup: 3769
    e = Env(parent)
    e.declare(['bundleName', 'i', 'id', 'itemData', 'itemName', 'k', 'kFields', 'n', 'q', 'qty', 'room', 'vFields'])
    e.local['arguments'] = Array(args)
    e.local['xmlDoc'] = (args[0] if len(args) > 0 and args[0] is not U else U)
    e.local['saveInfo'] = (args[1] if len(args) > 1 and args[1] is not U else U)
    e.local['input'] = (args[2] if len(args) > 2 and args[2] is not U else U)
    e.local['output'] = (args[3] if len(args) > 3 and args[3] is not U else U)
    e.local['meta'] = (args[4] if len(args) > 4 and args[4] is not U else U)
    put(e['meta'], 'roomID', Obj({'Pantry': 0, 'Crafts Room': 1, 'Fish Tank': 2, 'Boiler Room': 3, 'Vault': 4, 'Bulletin Board': 5, 'Abandoned Joja Mart': 6}))
    put(e['meta'], 'quality', Obj({'1': 'Silver', '2': 'Gold', '4': 'Iridium'}))
    put(e['meta'], 'bundleRoom', Obj({}))
    for _key166 in keys(e['input']):
        e.set('k', _key166)
        if truth(call(get(e['input'], 'hasOwnProperty'), e['k'])):
            e.set('kFields', call(get(e['k'], 'split'), '/'))
            e.set('room', get(e['kFields'], 0))
            e.set('id', get(e['kFields'], 1))
            e.set('vFields', call(get(get(e['input'], e['k']), 'split'), '/'))
            e.set('bundleName', get(e['vFields'], 0))
            e.set('itemData', call(get(get(e['vFields'], 2), 'split'), ' '))
            e.set('qty', get(e['vFields'], 4))
            if truth(unary('!', call(get(e['output'], 'hasOwnProperty'), get(get(e['meta'], 'roomID'), e['room'])))):
                put(e['output'], get(get(e['meta'], 'roomID'), e['room']), Obj({'name': e['room'], 'bundles': Obj({})}))
            put(get(get(e['output'], get(get(e['meta'], 'roomID'), e['room'])), 'bundles'), e['id'], Obj({'name': e['bundleName'], 'qty': e['qty'], 'items': Array([])}))
            put(get(e['meta'], 'bundleRoom'), e['id'], get(get(e['meta'], 'roomID'), e['room']))
            e.set('i', 0)
            while truth(binary('<', e['i'], get(e['itemData'], 'length'))):
                e.set('itemName', (get(get(e['saveInfo'], 'objects'), get(e['itemData'], e['i'])) if truth(call(get(get(e['saveInfo'], 'objects'), 'hasOwnProperty'), get(e['itemData'], e['i']))) else binary('+', 'Object ID ', get(e['itemData'], e['i']))))
                e.set('n', (binary('+', get(e['itemData'], binary('+', e['i'], 1)), 'x ') if truth(binary('>', call(e['Number'], get(e['itemData'], binary('+', e['i'], 1))), 1)) else ''))
                e.set('q', (binary('+', get(get(e['meta'], 'quality'), get(e['itemData'], binary('+', e['i'], 2))), ' ') if truth(call(get(get(e['meta'], 'quality'), 'hasOwnProperty'), get(e['itemData'], binary('+', e['i'], 2)))) else ''))
                if truth(binary('===', get(e['itemData'], e['i']), '-1')):
                    call(get(get(get(get(get(e['output'], get(get(e['meta'], 'roomID'), e['room'])), 'bundles'), e['id']), 'items'), 'push'), binary('+', call(e['addCommas'], get(e['itemData'], binary('+', e['i'], 1))), 'g'))
                else:
                    call(get(get(get(get(get(e['output'], get(get(e['meta'], 'roomID'), e['room'])), 'bundles'), e['id']), 'items'), 'push'), binary('+', binary('+', e['n'], e['q']), call(e['wikify'], e['itemName'])))
                e.set('i', binary('+', e['i'], 3))
            if truth(binary('===', e['qty'], '')):
                put(get(get(get(e['output'], get(get(e['meta'], 'roomID'), e['room'])), 'bundles'), e['id']), 'qty', get(get(get(get(get(e['output'], get(get(e['meta'], 'roomID'), e['room'])), 'bundles'), e['id']), 'items'), 'length'))
    return U


def callback_168(parent, this, args):
    # Upstream checkup: 3910
    e = Env(parent)
    e.declare([])
    e.local['arguments'] = Array(args)
    put(e['rawData'], call(get(call(get(call(e['$'], this), 'find'), 'key > string'), 'text')), call(get(call(get(call(e['$'], this), 'find'), 'value > string'), 'text')))
    return U


def callback_169(parent, this, args):
    # Upstream checkup: 3917
    e = Env(parent)
    e.declare([])
    e.local['arguments'] = Array(args)
    if truth(binary('===', call(get(call(e['$'], this), 'text')), 'true')):
        update_env(e, 'ccHave', 1, False)
        put(e['done'], e['r'], 1)
    update_env(e, 'r', 1, False)
    return U


def callback_171(parent, this, args):
    # Upstream checkup: 3930
    e = Env(parent)
    e.declare([])
    e.local['arguments'] = Array(args)
    if truth(binary('===', call(get(call(e['$'], this), 'text')), 'true')):
        update_prop(e['bundleHave'], e['id'], 1, False)
        put(get(e['itemsHave'], e['id']), e['i'], True)
    update_env(e, 'i', 1, False)
    return U


def callback_170(parent, this, args):
    # Upstream checkup: 3925
    e = Env(parent)
    e.declare([])
    e.local['arguments'] = Array(args)
    e.set('id', call(get(call(get(call(e['$'], this), 'find'), 'key > int'), 'text')))
    put(e['bundleHave'], e['id'], 0)
    put(e['itemsHave'], e['id'], Obj({}))
    e.set('i', 0)
    call(get(call(get(call(e['$'], this), 'find'), 'ArrayOfBoolean > boolean'), 'each'), Fn(callback_171, e))
    return U


def callback_172(parent, this, args):
    # Upstream checkup: 3941
    e = Env(parent)
    e.declare([])
    e.local['arguments'] = Array(args)
    e.local['id'] = (args[0] if len(args) > 0 and args[0] is not U else U)
    if truth(call(get(get(get(get(e['saveInfo'], 'data'), get(e['saveInfo'], 'farmerId')), 'mailReceived'), 'hasOwnProperty'), e['id'])):
        update_env(e, 'jojaHave', 1, False)
        put(e['done'], get(e['jojaMail'], e['id']), True)
    return U


def callback_178(parent, this, args):
    # Upstream checkup: 4023
    e = Env(parent)
    e.declare([])
    e.local['arguments'] = Array(args)
    e.local['e'] = (args[0] if len(args) > 0 and args[0] is not U else U)
    e.local['i'] = (args[1] if len(args) > 1 and args[1] is not U else U)
    e.local['a'] = (args[2] if len(args) > 2 and args[2] is not U else U)
    if truth(unary('!', call(get(get(e['itemsHave'], e['b']), 'hasOwnProperty'), e['i']))):
        call(get(e['possibles'], 'push'), get(get(get(get(get(e['bundleData'], e['r']), 'bundles'), e['b']), 'items'), e['i']))
    return U


def parseBundles_167(parent, this, args):
    # Upstream checkup: 3817
    e = Env(parent)
    e.declare(['anchor', 'b', 'bundleData', 'bundleHave', 'bundleNeed', 'ccCount', 'ccEvent', 'ccHave', 'ccLoc', 'ccMail', 'defaultData', 'det_class', 'done', 'eventToCheck', 'farmer', 'hasDetails', 'hasSeenCeremony', 'hybrid', 'hybridLeft', 'i', 'id', 'isJojaMember', 'itemsHave', 'jojaCount', 'jojaEvent', 'jojaHave', 'jojaMail', 'meta', 'need', 'output', 'possibles', 'price', 'project', 'r', 'rawData', 'room', 'sum_class', 'temp', 'title', 'version'])
    e.local['arguments'] = Array(args)
    e.local['xmlDoc'] = (args[0] if len(args) > 0 and args[0] is not U else U)
    e.local['saveInfo'] = (args[1] if len(args) > 1 and args[1] is not U else U)
    e.set('title', 'Community Center / Joja Community Development')
    e.set('anchor', call(e['makeAnchor'], e['title']))
    e.set('version', '1.5')
    e.set('sum_class', call(e['getSummaryClass'], e['saveInfo'], e['version']))
    e.set('det_class', call(e['getDetailsClass'], e['saveInfo'], e['version']))
    e.set('output', '')
    e.set('meta', Obj({}))
    e.set('farmer', call(get(call(get(call(e['$'], e['xmlDoc']), 'find'), 'player > name'), 'html')))
    e.set('hasDetails', False)
    e.set('isJojaMember', 0)
    e.set('room', Obj({}))
    e.set('bundleHave', Obj({}))
    e.set('ccMail', Obj({'ccBoilerRoom': 3, 'ccCraftsRoom': 1, 'ccPantry': 0, 'ccFishTank': 2, 'ccVault': 4, 'ccBulletin': 5}))
    e.set('ccCount', 6)
    e.set('ccHave', 0)
    e.set('ccEvent', '191393')
    e.set('project', Array(['Greenhouse', 'Bridge', 'Panning', 'Minecarts', 'Bus']))
    e.set('price', Array(['35,000g', '25,000g', '20,000g', '15,000g', '40,000g']))
    e.set('jojaMail', Obj({'jojaBoilerRoom': 3, 'jojaCraftsRoom': 1, 'jojaPantry': 0, 'jojaFishTank': 2, 'jojaVault': 4}))
    e.set('jojaCount', 5)
    e.set('jojaHave', 0)
    e.set('jojaEvent', '502261')
    e.set('eventToCheck', '')
    e.set('hasSeenCeremony', 0)
    e.set('done', Obj({}))
    e.set('hybrid', 0)
    e.set('hybridLeft', 0)
    e.set('itemsHave', Obj({}))
    e.set('bundleNeed', Array([]))
    e.set('need', Array([]))
    e.set('ccLoc', call(get(call(e['$'], e['xmlDoc']), 'find'), binary('+', binary('+', 'locations > GameLocation[', get(e['saveInfo'], 'ns_prefix')), "\\:type='CommunityCenter']")))
    e.set('bundleData', Obj({}))
    e.set('rawData', Obj({}))
    e.set('defaultData', table(17))
    if truth(binary('<', call(e['compareSemVer'], get(e['saveInfo'], 'version'), e['version']), 0)):
        call(e['parseBundleData'], e['xmlDoc'], e['saveInfo'], e['defaultData'], e['bundleData'], e['meta'])
    else:
        call(get(call(get(call(e['$'], e['xmlDoc']), 'find'), 'bundleData > item'), 'each'), Fn(callback_168, e))
        call(e['parseBundleData'], e['xmlDoc'], e['saveInfo'], e['rawData'], e['bundleData'], e['meta'])
    e.set('r', 0)
    call(get(call(get(call(e['$'], e['ccLoc']), 'find'), 'areasComplete > boolean'), 'each'), Fn(callback_169, e))
    call(get(call(get(call(e['$'], e['ccLoc']), 'find'), 'bundles > item'), 'each'), Fn(callback_170, e))
    if truth(call(get(get(get(get(e['saveInfo'], 'data'), get(e['saveInfo'], 'farmerId')), 'mailReceived'), 'hasOwnProperty'), 'JojaMember')):
        e.set('isJojaMember', True)
    call(get(call(get(e['Object'], 'keys'), e['jojaMail']), 'forEach'), Fn(callback_172, e))
    if truth((e['isJojaMember'] if truth(_logic173 := binary('>', e['ccHave'], 0)) else _logic173)):
        e.set('hybrid', True)
    e.set('hybridLeft', binary('-', e['jojaCount'], e['ccHave']))
    if truth(call(get(e['done'], 'hasOwnProperty'), get(e['ccMail'], 'ccBulletin'))):
        update_env(e, 'hybridLeft', 1, False)
    e.set('eventToCheck', (e['jojaEvent'] if truth(e['isJojaMember']) else e['ccEvent']))
    if truth(call(get(get(get(get(e['saveInfo'], 'data'), get(e['saveInfo'], 'farmerId')), 'eventsSeen'), 'hasOwnProperty'), e['eventToCheck'])):
        e.set('hasSeenCeremony', True)
    e.set('output', binary('+', e['output'], binary('+', binary('+', binary('+', binary('+', '<div class="', e['anchor']), '_summary '), e['sum_class']), '">')))
    if truth(e['isJojaMember']):
        if truth(e['hybrid']):
            e.set('output', binary('+', e['output'], binary('+', binary('+', binary('+', binary('+', '<span class="result">', e['farmer']), ' completed '), e['ccHave']), ' Community Center room(s) and then became a Joja member.</span><br />\n')))
            e.set('output', binary('+', e['output'], binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', '<span class="result">', e['farmer']), ' has since completed '), e['jojaHave']), ' of the remaining '), e['hybridLeft']), ' projects on the Community Development Form.</span><br />\n')))
        else:
            e.set('output', binary('+', e['output'], binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', '<span class="result">', e['farmer']), ' is a Joja member and has completed '), e['jojaHave']), ' of the '), e['jojaCount']), ' projects on the Community Development Form.</span><br />\n')))
        e.set('hybridLeft', binary('-', e['hybridLeft'], e['jojaHave']))
        e.set('output', binary('+', e['output'], binary('+', binary('+', binary('+', '<span class="result">', e['farmer']), (' has' if truth(e['hasSeenCeremony']) else ' has not')), ' attended the completion ceremony</span><br />\n<ul class="ach_list"><li>')))
        e.set('output', binary('+', e['output'], call(e['getAchieveImpossibleString'], 'Local Legend', 'restore the Pelican Town Community Center')))
        e.set('output', binary('+', e['output'], '</li><li>\n'))
        if truth(unary('!', e['hasSeenCeremony'])):
            if truth(binary('>', e['hybridLeft'], 0)):
                e.set('temp', binary('+', e['hybridLeft'], ' more project(s) and the ceremony'))
                for _key174 in keys(e['ccMail']):
                    e.set('id', _key174)
                    if truth((binary('!==', e['id'], 'ccBulletin') if truth(_logic175 := call(get(e['ccMail'], 'hasOwnProperty'), e['id'])) else _logic175)):
                        if truth(unary('!', call(get(e['done'], 'hasOwnProperty'), get(e['ccMail'], e['id'])))):
                            call(get(e['need'], 'push'), binary('+', binary('+', binary('+', binary('+', '<li> Purchase ', get(e['project'], get(e['ccMail'], e['id']))), ' project for '), get(e['price'], get(e['ccMail'], e['id']))), '</li>'))
            else:
                e.set('temp', ' to attend the ceremony')
            call(get(e['need'], 'push'), '<li>Attend the completion ceremony at the Joja Warehouse</li>')
        e.set('output', binary('+', e['output'], (call(e['getAchieveString'], 'Joja Co. Member Of The Year', '', 1) if truth(e['hasSeenCeremony']) else binary('+', call(e['getAchieveString'], 'Joja Co. Member Of The Year', '', 0), e['temp']))))
        e.set('output', binary('+', e['output'], '</li></ul>\n'))
    else:
        e.set('output', binary('+', e['output'], binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', '<span class="result">', e['farmer']), ' is not a Joja member and has completed '), e['ccHave']), ' of the '), e['ccCount']), ' Community Center rooms.</span><br />\n')))
        e.set('output', binary('+', e['output'], binary('+', binary('+', binary('+', '<span class="result">', e['farmer']), (' has' if truth(e['hasSeenCeremony']) else ' has not')), ' attended the completion ceremony</span><br />\n<ul class="ach_list"><li>')))
        if truth(binary('===', e['ccHave'], 0)):
            e.set('output', binary('+', e['output'], binary('+', call(e['getAchieveString'], 'Joja Co. Member Of The Year', '', 0), 'to become a Joja member and purchase all community development perks')))
        else:
            if truth(binary('<', e['ccHave'], e['ccCount'])):
                e.set('output', binary('+', e['output'], binary('+', binary('+', binary('+', call(e['getAchieveString'], 'Joja Co. Member Of The Year', '', 0), 'to become a Joja member and purchase any remaining community development perks ('), e['hybridLeft']), ' left)')))
            else:
                e.set('output', binary('+', e['output'], call(e['getAchieveImpossibleString'], 'Joja Co. Member Of The Year', 'become a Joja member and purchase all community development perks')))
        e.set('output', binary('+', e['output'], '</li><li>\n'))
        if truth(unary('!', e['hasSeenCeremony'])):
            if truth(binary('<', e['ccHave'], e['ccCount'])):
                e.set('temp', binary('+', binary('-', e['ccCount'], e['ccHave']), ' more room(s) and the ceremony'))
                for _key176 in keys(e['ccMail']):
                    e.set('id', _key176)
                    if truth(call(get(e['ccMail'], 'hasOwnProperty'), e['id'])):
                        e.set('r', get(e['ccMail'], e['id']))
                        if truth(unary('!', call(get(e['done'], 'hasOwnProperty'), e['r']))):
                            e.set('bundleNeed', Array([]))
                            if truth(call(get(e['bundleData'], 'hasOwnProperty'), e['r'])):
                                for _key177 in keys(get(get(e['bundleData'], e['r']), 'bundles')):
                                    e.set('b', _key177)
                                    if truth(call(get(get(get(e['bundleData'], e['r']), 'bundles'), 'hasOwnProperty'), e['b'])):
                                        if truth(binary('<', get(e['bundleHave'], e['b']), get(get(get(get(e['bundleData'], e['r']), 'bundles'), e['b']), 'qty'))):
                                            e.set('possibles', Array([]))
                                            call(get(get(get(get(get(e['bundleData'], e['r']), 'bundles'), e['b']), 'items'), 'forEach'), Fn(callback_178, e))
                                            call(get(e['bundleNeed'], 'push'), binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', '<li>', get(get(get(get(e['bundleData'], e['r']), 'bundles'), e['b']), 'name')), ' Bundle -- need '), binary('-', get(get(get(get(e['bundleData'], e['r']), 'bundles'), e['b']), 'qty'), get(e['bundleHave'], e['b']))), ' of: '), call(get(e['possibles'], 'join'), ', ')), '</li>'))
                            call(get(e['need'], 'push'), binary('+', binary('+', binary('+', binary('+', '<li> ', call(e['wikify'], get(get(e['bundleData'], e['r']), 'name'), 'Bundles')), '<ol>'), call(get(call(get(e['bundleNeed'], 'sort')), 'join'), '')), '</ol></li>'))
            else:
                e.set('temp', ' to attend the ceremony')
            call(get(e['need'], 'push'), '<li>Attend the re-opening ceremony at the Community Center</li>')
        e.set('output', binary('+', e['output'], (call(e['getAchieveString'], 'Local Legend', '', 1) if truth((e['hasSeenCeremony'] if truth(_logic179 := binary('>=', e['ccHave'], e['ccCount'])) else _logic179)) else binary('+', call(e['getAchieveString'], 'Local Legend', '', 0), e['temp']))))
        e.set('output', binary('+', e['output'], '</li></ul></div>'))
    if truth(binary('>', get(e['need'], 'length'), 0)):
        e.set('hasDetails', True)
        e.set('output', binary('+', e['output'], binary('+', binary('+', binary('+', binary('+', '<div class="', e['anchor']), '_details '), e['det_class']), '">')))
        e.set('output', binary('+', e['output'], binary('+', binary('+', '<span class="need">Left to do:<ol>', call(get(call(get(e['need'], 'sort')), 'join'), '')), '</ol></span></div>')))
    e.set('output', binary('+', binary('+', call(e['getSectionHeader'], e['saveInfo'], e['title'], e['anchor'], e['hasDetails'], e['version']), e['output']), call(e['getSectionFooter'])))
    return e['output']
    return U


def callback_181(parent, this, args):
    # Upstream checkup: 4077
    e = Env(parent)
    e.declare([])
    e.local['arguments'] = Array(args)
    if truth(binary('===', call(get(call(e['$'], this), 'text')), 'Stone Junimo')):
        put(e['meta'], 'hasStoneJunimo', True)
        return False
    return U


def callback_182(parent, this, args):
    # Upstream checkup: 4085
    e = Env(parent)
    e.declare(['loc', 'x', 'y'])
    e.local['arguments'] = Array(args)
    if truth(binary('===', call(get(call(e['$'], this), 'text')), 'Stone Junimo')):
        e.set('loc', call(get(call(get(call(get(call(e['$'], this), 'parents'), 'GameLocation'), 'children'), 'name'), 'text')))
        if truth(binary('===', e['loc'], 'Town')):
            e.set('x', call(get(call(get(call(get(call(e['$'], this), 'parents'), 'item'), 'find'), 'key > Vector2 > X'), 'text')))
            e.set('y', call(get(call(get(call(get(call(e['$'], this), 'parents'), 'item'), 'find'), 'key > Vector2 > Y'), 'text')))
            if truth((_logic183 if truth(_logic183 := binary('!==', e['x'], '57')) else binary('!==', e['y'], '16'))):
                put(e['meta'], 'hasStoneJunimo', True)
                return False
        else:
            put(e['meta'], 'hasStoneJunimo', True)
            return False
    return U


def parseSecretNotes_180(parent, this, args):
    # Upstream checkup: 4057
    e = Env(parent)
    e.declare(['anchor', 'det_class', 'meta', 'output', 'playerOutput', 'sum_class', 'table', 'title', 'version'])
    e.local['arguments'] = Array(args)
    e.local['xmlDoc'] = (args[0] if len(args) > 0 and args[0] is not U else U)
    e.local['saveInfo'] = (args[1] if len(args) > 1 and args[1] is not U else U)
    e.set('title', 'Secret Notes')
    e.set('anchor', call(e['makeAnchor'], e['title']))
    e.set('version', '1.3')
    e.set('sum_class', call(e['getSummaryClass'], e['saveInfo'], e['version']))
    e.set('det_class', call(e['getDetailsClass'], e['saveInfo'], e['version']))
    e.set('output', '')
    e.set('playerOutput', '')
    e.set('meta', Obj({'hasDetails': False, 'anchor': e['anchor'], 'sum_class': e['sum_class'], 'det_class': e['det_class']}))
    e.set('table', Array([]))
    put(e['meta'], 'hasStoneJunimo', False)
    if truth(binary('<', call(e['compareSemVer'], get(e['saveInfo'], 'version'), '1.3'), 0)):
        return ''
    call(get(call(get(call(e['$'], e['xmlDoc']), 'find'), 'Item > name'), 'each'), Fn(callback_181, e))
    if truth(unary('!', get(e['meta'], 'hasStoneJunimo'))):
        call(get(call(get(call(e['$'], e['xmlDoc']), 'find'), 'Object > name'), 'each'), Fn(callback_182, e))
    put(e['table'], 0, call(e['parsePlayerSecretNotes'], call(get(call(e['$'], e['xmlDoc']), 'find'), 'SaveGame > player'), e['saveInfo'], e['meta']))
    call(e['parseFarmhands'], e['xmlDoc'], e['saveInfo'], e['table'], e['parsePlayerSecretNotes'], e['meta'])
    e.set('playerOutput', binary('+', e['playerOutput'], call(e['printTranspose'], e['table'])))
    e.set('output', binary('+', binary('+', call(e['getSectionHeader'], e['saveInfo'], e['title'], e['anchor'], get(e['meta'], 'hasDetails'), e['version']), e['playerOutput']), call(e['getSectionFooter'])))
    return e['output']
    return U


def callback_185(parent, this, args):
    # Upstream checkup: 4167
    e = Env(parent)
    e.declare([])
    e.local['arguments'] = Array(args)
    e.local['id'] = (args[0] if len(args) > 0 and args[0] is not U else U)
    if truth(call(get(get(get(get(e['saveInfo'], 'data'), e['umid']), 'mailReceived'), 'hasOwnProperty'), e['id'])):
        put(e['rewards'], get(e['rewardMail'], e['id']), True)
        update_env(e, 'found_rewards', 1, False)
    return U


def callback_186(parent, this, args):
    # Upstream checkup: 4188
    e = Env(parent)
    e.declare([])
    e.local['arguments'] = Array(args)
    if truth(binary('<', call(e['Number'], call(get(call(e['$'], this), 'text'))), 1000)):
        if truth(binary('>', call(e['Number'], call(get(call(e['$'], this), 'text'))), e['note_count'])):
            update_env(e, 'mod_count', 1, False)
        else:
            put(e['notes'], call(get(call(e['$'], this), 'text')), True)
            update_env(e, 'found_notes', 1, False)
    return U


def parsePlayerSecretNotes_184(parent, this, args):
    # Upstream checkup: 4110
    e = Env(parent)
    e.declare(['extra', 'farmer', 'found_notes', 'found_rewards', 'hasMagnifyingGlass', 'hasSeenKrobus', 'i', 'isJojaMember', 'mod_count', 'need', 'note_count', 'notes', 'output', 'rewardMail', 'reward_count', 'reward_skip', 'reward_start', 'rewards', 'table', 'umid'])
    e.local['arguments'] = Array(args)
    e.local['player'] = (args[0] if len(args) > 0 and args[0] is not U else U)
    e.local['saveInfo'] = (args[1] if len(args) > 1 and args[1] is not U else U)
    e.local['meta'] = (args[2] if len(args) > 2 and args[2] is not U else U)
    e.set('output', '')
    e.set('table', Array([]))
    e.set('farmer', call(get(call(get(call(e['$'], e['player']), 'children'), 'name'), 'html')))
    e.set('hasSeenKrobus', False)
    e.set('hasMagnifyingGlass', False)
    e.set('isJojaMember', False)
    e.set('umid', call(get(call(get(call(e['$'], e['player']), 'children'), 'UniqueMultiplayerID'), 'text')))
    e.set('notes', Obj({}))
    e.set('need', Array([]))
    e.set('rewards', Obj({}))
    e.set('reward_skip', Obj({}))
    e.set('found_notes', 0)
    e.set('found_rewards', 0)
    e.set('note_count', 23)
    e.set('mod_count', 0)
    e.set('reward_start', 13)
    e.set('reward_count', binary('+', binary('-', e['note_count'], e['reward_start']), 1))
    if truth(binary('>=', call(e['compareSemVer'], get(e['saveInfo'], 'version'), '1.4'), 0)):
        e.set('note_count', 25)
        update_env(e, 'reward_count', 1, False)
        put(e['reward_skip'], 24, True)
    if truth(binary('>=', call(e['compareSemVer'], get(e['saveInfo'], 'version'), '1.6'), 0)):
        e.set('note_count', 27)
        put(e['reward_skip'], 26, True)
        put(e['reward_skip'], 27, True)
        if truth(call(get(get(get(get(e['saveInfo'], 'data'), e['umid']), 'mailReceived'), 'hasOwnProperty'), 'HasMagnifyingGlass')):
            e.set('hasMagnifyingGlass', True)
    else:
        e.set('hasMagnifyingGlass', binary('===', call(get(call(get(call(e['$'], e['player']), 'children'), 'hasMagnifyingGlass'), 'text')), 'true'))
    if truth(call(get(get(get(get(e['saveInfo'], 'data'), e['umid']), 'eventsSeen'), 'hasOwnProperty'), '520702')):
        e.set('hasSeenKrobus', True)
    if truth(call(get(get(get(get(e['saveInfo'], 'data'), e['umid']), 'eventsSeen'), 'hasOwnProperty'), '2120303')):
        put(e['rewards'], 23, True)
        update_env(e, 'found_rewards', 1, False)
    e.set('rewardMail', table(18))
    call(get(call(get(e['Object'], 'keys'), e['rewardMail']), 'forEach'), Fn(callback_185, e))
    if truth(call(get(get(get(get(e['saveInfo'], 'data'), e['umid']), 'mailReceived'), 'hasOwnProperty'), 'JojaMember')):
        e.set('isJojaMember', True)
    if truth(e['isJojaMember']):
        update_env(e, 'reward_count', -1, False)
        put(e['reward_skip'], 14, True)
    else:
        if truth(get(e['meta'], 'hasStoneJunimo')):
            put(e['rewards'], 14, True)
            update_env(e, 'found_rewards', 1, False)
    e.set('output', binary('+', e['output'], binary('+', binary('+', binary('+', binary('+', '<div class="', get(e['meta'], 'anchor')), '_summary '), get(e['meta'], 'sum_class')), '">')))
    e.set('output', binary('+', e['output'], binary('+', binary('+', binary('+', binary('+', '<span class="result">', e['farmer']), ' has '), ('' if truth(e['hasSeenKrobus']) else 'not ')), ' seen the Shadow Guy at the Bus Stop.</span><br />\n')))
    e.set('output', binary('+', e['output'], binary('+', binary('+', binary('+', binary('+', '<span class="result">', e['farmer']), ' has '), ('' if truth(e['hasMagnifyingGlass']) else 'not ')), ' found the Magnifying Glass.</span><br />\n')))
    call(get(call(get(call(e['$'], e['player']), 'find'), 'secretNotesSeen > int'), 'each'), Fn(callback_186, e))
    e.set('output', binary('+', e['output'], binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', '<span class="result">', e['farmer']), ' has read '), e['found_notes']), ' of '), e['note_count']), ' secret notes.</span><br />\n')))
    if truth(binary('>', e['mod_count'], 0)):
        e.set('output', binary('+', e['output'], binary('+', binary('+', binary('+', binary('+', '<span class="result note">', e['farmer']), ' has read '), e['mod_count']), ' mod secret note(s).</span><br />\n')))
    e.set('output', binary('+', e['output'], '<ul class="ach_list"><li>'))
    e.set('output', binary('+', e['output'], (call(e['getMilestoneString'], 'Read all the secret notes', 1) if truth(binary('>=', e['found_notes'], e['note_count'])) else binary('+', binary('+', call(e['getMilestoneString'], 'Read all the secret notes', 0), binary('-', e['note_count'], e['found_notes'])), ' more'))))
    e.set('output', binary('+', e['output'], '</li></ul></div>'))
    if truth(binary('<', e['found_notes'], e['note_count'])):
        e.set('i', 1)
        while truth(binary('<=', e['i'], e['note_count'])):
            if truth(unary('!', call(get(e['notes'], 'hasOwnProperty'), e['i']))):
                call(get(e['need'], 'push'), binary('+', binary('+', '<li>', call(e['wikify'], binary('+', 'Secret Note #', e['i']), 'Secret Notes')), '</li>'))
            update_env(e, 'i', 1, False)
        if truth(binary('>', get(e['need'], 'length'), 0)):
            put(e['meta'], 'hasDetails', True)
            e.set('output', binary('+', e['output'], binary('+', binary('+', binary('+', binary('+', '<div class="', get(e['meta'], 'anchor')), '_details '), get(e['meta'], 'det_class')), '">')))
            e.set('output', binary('+', e['output'], binary('+', binary('+', '<span class="need">Left to read:<ol>', call(get(e['need'], 'join'), '')), '</ol></span></div>')))
    call(get(e['table'], 'push'), e['output'])
    e.set('output', binary('+', binary('+', binary('+', binary('+', '<div class="', get(e['meta'], 'anchor')), '_summary '), get(e['meta'], 'sum_class')), '">'))
    e.set('output', binary('+', e['output'], binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', '<span class="result">', e['farmer']), ' has found the rewards from  '), e['found_rewards']), ' of '), e['reward_count']), ' secret notes.</span><br />\n')))
    e.set('output', binary('+', e['output'], '<ul class="ach_list"><li>'))
    e.set('output', binary('+', e['output'], (call(e['getMilestoneString'], 'Find all the secret note rewards', 1) if truth(binary('>=', e['found_rewards'], e['reward_count'])) else binary('+', binary('+', call(e['getMilestoneString'], 'Find all the secret note rewards', 0), binary('-', e['reward_count'], e['found_rewards'])), ' more'))))
    e.set('output', binary('+', e['output'], '</li></ul></div>'))
    if truth(binary('<', e['found_rewards'], e['reward_count'])):
        e.set('need', Array([]))
        e.set('i', e['reward_start'])
        while truth(binary('<=', e['i'], e['note_count'])):
            if truth((unary('!', call(get(e['rewards'], 'hasOwnProperty'), e['i'])) if truth(_logic187 := unary('!', call(get(e['reward_skip'], 'hasOwnProperty'), e['i']))) else _logic187)):
                e.set('extra', '')
                if truth(binary('==', e['i'], 14)):
                    e.set('extra', ' (Note: may be inaccurate if item was collected and destroyed.)')
                call(get(e['need'], 'push'), binary('+', binary('+', binary('+', '<li> Reward from ', call(e['wikify'], binary('+', 'Secret Note #', e['i']), 'Secret Notes')), e['extra']), '</li>'))
            update_env(e, 'i', 1, False)
        if truth(binary('>', get(e['need'], 'length'), 0)):
            put(e['meta'], 'hasDetails', True)
            e.set('output', binary('+', e['output'], binary('+', binary('+', binary('+', binary('+', '<div class="', get(e['meta'], 'anchor')), '_details '), get(e['meta'], 'det_class')), '">')))
            e.set('output', binary('+', e['output'], binary('+', binary('+', '<span class="need">Left to find:<ol>', call(get(e['need'], 'join'), '')), '</ol></span></div>')))
    call(get(e['table'], 'push'), e['output'])
    return e['table']
    return U


def parseJournalScraps_188(parent, this, args):
    # Upstream checkup: 4251
    e = Env(parent)
    e.declare(['anchor', 'det_class', 'meta', 'output', 'playerOutput', 'sum_class', 'table', 'title', 'version'])
    e.local['arguments'] = Array(args)
    e.local['xmlDoc'] = (args[0] if len(args) > 0 and args[0] is not U else U)
    e.local['saveInfo'] = (args[1] if len(args) > 1 and args[1] is not U else U)
    e.set('title', 'Journal Scraps')
    e.set('anchor', call(e['makeAnchor'], e['title']))
    e.set('version', '1.5')
    e.set('sum_class', call(e['getSummaryClass'], e['saveInfo'], e['version']))
    e.set('det_class', call(e['getDetailsClass'], e['saveInfo'], e['version']))
    e.set('output', '')
    e.set('playerOutput', '')
    e.set('meta', Obj({'hasDetails': False, 'anchor': e['anchor'], 'sum_class': e['sum_class'], 'det_class': e['det_class']}))
    e.set('table', Array([]))
    if truth(binary('<', call(e['compareSemVer'], get(e['saveInfo'], 'version'), e['version']), 0)):
        return ''
    put(e['table'], 0, call(e['parsePlayerJournalScraps'], call(get(call(e['$'], e['xmlDoc']), 'find'), 'SaveGame > player'), e['saveInfo'], e['meta']))
    call(e['parseFarmhands'], e['xmlDoc'], e['saveInfo'], e['table'], e['parsePlayerJournalScraps'], e['meta'])
    e.set('playerOutput', binary('+', e['playerOutput'], call(e['printTranspose'], e['table'])))
    e.set('output', binary('+', binary('+', call(e['getSectionHeader'], e['saveInfo'], e['title'], e['anchor'], get(e['meta'], 'hasDetails'), e['version']), e['playerOutput']), call(e['getSectionFooter'])))
    return e['output']
    return U


def callback_190(parent, this, args):
    # Upstream checkup: 4294
    e = Env(parent)
    e.declare([])
    e.local['arguments'] = Array(args)
    e.local['id'] = (args[0] if len(args) > 0 and args[0] is not U else U)
    if truth(call(get(get(get(get(e['saveInfo'], 'data'), e['umid']), 'mailReceived'), 'hasOwnProperty'), e['id'])):
        put(e['rewards'], get(e['rewardMail'], e['id']), True)
        update_env(e, 'found_rewards', 1, False)
    return U


def callback_191(parent, this, args):
    # Upstream checkup: 4310
    e = Env(parent)
    e.declare([])
    e.local['arguments'] = Array(args)
    if truth(binary('>=', call(e['Number'], call(get(call(e['$'], this), 'text'))), 1000)):
        if truth(binary('>=', call(e['Number'], call(get(call(e['$'], this), 'text'))), 1012)):
            update_env(e, 'mod_count', 1, False)
        else:
            put(e['notes'], call(get(call(e['$'], this), 'text')), True)
            update_env(e, 'found_notes', 1, False)
    return U


def callback_192(parent, this, args):
    # Upstream checkup: 4344
    e = Env(parent)
    e.declare([])
    e.local['arguments'] = Array(args)
    if truth(binary('===', call(get(call(e['$'], this), 'text')), 'Mermaid')):
        put(e['rewards'], 1009, True)
        update_env(e, 'found_rewards', 1, False)
        return False
    return U


def parsePlayerJournalScraps_189(parent, this, args):
    # Upstream checkup: 4273
    e = Env(parent)
    e.declare(['extra', 'farmer', 'found_notes', 'found_rewards', 'hasVisitedIsland', 'i', 'k', 'mod_count', 'need', 'note_count', 'notes', 'output', 'rewardMail', 'reward_count', 'rewards', 'table', 'umid'])
    e.local['arguments'] = Array(args)
    e.local['player'] = (args[0] if len(args) > 0 and args[0] is not U else U)
    e.local['saveInfo'] = (args[1] if len(args) > 1 and args[1] is not U else U)
    e.local['meta'] = (args[2] if len(args) > 2 and args[2] is not U else U)
    e.set('output', '')
    e.set('table', Array([]))
    e.set('farmer', call(get(call(get(call(e['$'], e['player']), 'children'), 'name'), 'html')))
    e.set('hasVisitedIsland', False)
    e.set('umid', call(get(call(get(call(e['$'], e['player']), 'children'), 'UniqueMultiplayerID'), 'text')))
    e.set('notes', Obj({}))
    e.set('need', Array([]))
    e.set('rewards', Obj({'1004': False, '1006': False, '1009': False, '1010': False}))
    e.set('found_notes', 0)
    e.set('found_rewards', 0)
    e.set('note_count', 11)
    e.set('reward_count', 4)
    e.set('mod_count', 0)
    e.set('rewardMail', Obj({'Island_W_BuriedTreasure2': 1006, 'Island_W_BuriedTreasure': 1004, 'Island_N_BuriedTreasure': 1010}))
    call(get(call(get(e['Object'], 'keys'), e['rewardMail']), 'forEach'), Fn(callback_190, e))
    if truth(call(get(get(get(get(e['saveInfo'], 'data'), e['umid']), 'mailReceived'), 'hasOwnProperty'), 'Visited_Island')):
        e.set('hasVisitedIsland', True)
    e.set('output', binary('+', e['output'], binary('+', binary('+', binary('+', binary('+', '<div class="', get(e['meta'], 'anchor')), '_summary '), get(e['meta'], 'sum_class')), '">')))
    e.set('output', binary('+', e['output'], binary('+', binary('+', binary('+', binary('+', '<span class="result">', e['farmer']), ' has '), ('' if truth(e['hasVisitedIsland']) else 'not ')), ' visited the Island.</span><br />\n')))
    e.set('output', binary('+', e['output'], '<ul class="ach_list"><li>'))
    e.set('output', binary('+', e['output'], (call(e['getAchieveString'], 'A Distant Shore', 'Reach Ginger Island', 1) if truth(e['hasVisitedIsland']) else binary('+', call(e['getAchieveString'], 'A Distant Shore', 'Reach Ginger Island', 0), ' to visit'))))
    e.set('output', binary('+', e['output'], '</li></ul></div>'))
    call(get(call(get(call(e['$'], e['player']), 'find'), 'secretNotesSeen > int'), 'each'), Fn(callback_191, e))
    e.set('output', binary('+', e['output'], binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', '<span class="result">', e['farmer']), ' has read '), e['found_notes']), ' of '), e['note_count']), ' journal scraps.</span><br />\n')))
    if truth(binary('>', e['mod_count'], 0)):
        e.set('output', binary('+', e['output'], binary('+', binary('+', binary('+', binary('+', '<span class="result note">', e['farmer']), ' has read '), e['mod_count']), ' mod journal scrap(s).</span><br />\n')))
    e.set('output', binary('+', e['output'], '<ul class="ach_list"><li>'))
    e.set('output', binary('+', e['output'], (call(e['getMilestoneString'], 'Read all the journal scraps', 1) if truth(binary('>=', e['found_notes'], e['note_count'])) else binary('+', binary('+', call(e['getMilestoneString'], 'Read all the journal scraps', 0), binary('-', e['note_count'], e['found_notes'])), ' more'))))
    e.set('output', binary('+', e['output'], '</li></ul></div>'))
    if truth(binary('<', e['found_notes'], e['note_count'])):
        e.set('i', 1)
        while truth(binary('<=', e['i'], e['note_count'])):
            if truth(unary('!', call(get(e['notes'], 'hasOwnProperty'), binary('+', 1000, call(e['Number'], e['i']))))):
                call(get(e['need'], 'push'), binary('+', binary('+', '<li>', call(e['wikify'], binary('+', 'Journal Scrap #', e['i']), 'Journal Scraps')), '</li>'))
            update_env(e, 'i', 1, False)
        if truth(binary('>', get(e['need'], 'length'), 0)):
            put(e['meta'], 'hasDetails', True)
            e.set('output', binary('+', e['output'], binary('+', binary('+', binary('+', binary('+', '<div class="', get(e['meta'], 'anchor')), '_details '), get(e['meta'], 'det_class')), '">')))
            e.set('output', binary('+', e['output'], binary('+', binary('+', '<span class="need">Left to read:<ol>', call(get(e['need'], 'join'), '')), '</ol></span></div>')))
    call(get(e['table'], 'push'), e['output'])
    call(get(call(get(call(get(call(get(call(e['$'], e['player']), 'parents'), 'SaveGame'), 'first')), 'find'), 'collectedNutTracker > string'), 'each'), Fn(callback_192, e))
    e.set('output', binary('+', binary('+', binary('+', binary('+', '<div class="', get(e['meta'], 'anchor')), '_summary '), get(e['meta'], 'sum_class')), '">'))
    e.set('output', binary('+', e['output'], binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', '<span class="result">', e['farmer']), ' has found the rewards from  '), e['found_rewards']), ' of '), e['reward_count']), ' journal scraps.</span><br />\n')))
    e.set('output', binary('+', e['output'], '<ul class="ach_list"><li>'))
    e.set('output', binary('+', e['output'], (call(e['getMilestoneString'], 'Find all the journal scrap rewards', 1) if truth(binary('>=', e['found_rewards'], e['reward_count'])) else binary('+', binary('+', call(e['getMilestoneString'], 'Find all the journal scrap rewards', 0), binary('-', e['reward_count'], e['found_rewards'])), ' more'))))
    e.set('output', binary('+', e['output'], '</li></ul></div>'))
    if truth(binary('<', e['found_rewards'], e['reward_count'])):
        e.set('need', Array([]))
        e.set('k', call(get(call(get(e['Object'], 'keys'), e['rewards']), 'sort')))
        for _key193 in keys(e['k']):
            e.set('i', _key193)
            if truth((unary('!', get(e['rewards'], get(e['k'], e['i']))) if truth(_logic194 := call(get(e['rewards'], 'hasOwnProperty'), get(e['k'], e['i']))) else _logic194)):
                e.set('extra', '')
                call(get(e['need'], 'push'), binary('+', binary('+', binary('+', '<li> Reward from ', call(e['wikify'], binary('+', 'Journal Scrap #', binary('-', call(e['Number'], get(e['k'], e['i'])), 1000)), 'Journal Scraps')), e['extra']), '</li>'))
        if truth(binary('>', get(e['need'], 'length'), 0)):
            put(e['meta'], 'hasDetails', True)
            e.set('output', binary('+', e['output'], binary('+', binary('+', binary('+', binary('+', '<div class="', get(e['meta'], 'anchor')), '_details '), get(e['meta'], 'det_class')), '">')))
            e.set('output', binary('+', e['output'], binary('+', binary('+', '<span class="need">Left to find:<ol>', call(get(e['need'], 'join'), '')), '</ol></span></div>')))
    call(get(e['table'], 'push'), e['output'])
    return e['table']
    return U


def callback_196(parent, this, args):
    # Upstream checkup: 4399
    e = Env(parent)
    e.declare([])
    e.local['arguments'] = Array(args)
    e.set('id', call(get(call(e['$'], this), 'text')))
    if truth(call(get(e['town'], 'hasOwnProperty'), e['id'])):
        put(e['found'], e['id'], True)
        update_env(e, 'found_count', 1, False)
    return U


def parseSpecialOrders_195(parent, this, args):
    # Upstream checkup: 4377
    e = Env(parent)
    e.declare(['anchor', 'det_class', 'found', 'found_count', 'hasWalnutRoomAccess', 'id', 'intro', 'meta', 'need', 'output', 'playerOutput', 'qi', 'sum_class', 'title', 'town', 'town_count', 'version'])
    e.local['arguments'] = Array(args)
    e.local['xmlDoc'] = (args[0] if len(args) > 0 and args[0] is not U else U)
    e.local['saveInfo'] = (args[1] if len(args) > 1 and args[1] is not U else U)
    e.set('title', 'Special Orders')
    e.set('anchor', call(e['makeAnchor'], e['title']))
    e.set('version', '1.5')
    e.set('sum_class', call(e['getSummaryClass'], e['saveInfo'], e['version']))
    e.set('det_class', call(e['getDetailsClass'], e['saveInfo'], e['version']))
    e.set('output', '')
    e.set('playerOutput', '')
    e.set('meta', Obj({'hasDetails': False, 'anchor': e['anchor'], 'sum_class': e['sum_class'], 'det_class': e['det_class']}))
    e.set('found', Obj({}))
    e.set('found_count', 0)
    e.set('need', Array([]))
    e.set('hasWalnutRoomAccess', False)
    e.set('town', table(19))
    e.set('town_count', get(call(get(e['Object'], 'keys'), e['town']), 'length'))
    e.set('qi', table(20))
    if truth(binary('<', call(e['compareSemVer'], get(e['saveInfo'], 'version'), e['version']), 0)):
        return ''
    call(get(call(get(call(e['$'], e['xmlDoc']), 'find'), 'completedSpecialOrders > string'), 'each'), Fn(callback_196, e))
    if truth(binary('>', get(e['saveInfo'], 'numPlayers'), 1)):
        e.set('intro', binary('+', binary('+', 'Inhabitants of ', get(e['saveInfo'], 'farmName')), ' Farm have'))
    else:
        e.set('intro', binary('+', get(get(e['saveInfo'], 'players'), get(e['saveInfo'], 'farmerId')), ' has'))
    e.set('output', binary('+', binary('+', binary('+', binary('+', '<div class="', get(e['meta'], 'anchor')), '_summary '), get(e['meta'], 'sum_class')), '">'))
    e.set('output', binary('+', e['output'], binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', '<span class="result">', e['intro']), ' completed '), e['found_count']), ' of '), e['town_count']), ' town special orders.</span><br />\n')))
    e.set('output', binary('+', e['output'], '<ul class="ach_list"><li>'))
    e.set('output', binary('+', e['output'], (call(e['getMilestoneString'], 'Complete all Special Orders', 1) if truth(binary('>=', e['found_count'], e['town_count'])) else binary('+', binary('+', call(e['getMilestoneString'], 'Complete all Special Orders', 0), binary('-', e['town_count'], e['found_count'])), ' more'))))
    e.set('output', binary('+', e['output'], '</li></ul></div>'))
    if truth(binary('<', e['found_count'], e['town_count'])):
        for _key197 in keys(e['town']):
            e.set('id', _key197)
            if truth(unary('!', call(get(e['found'], 'hasOwnProperty'), e['id']))):
                call(get(e['need'], 'push'), binary('+', binary('+', '<li>', call(e['wikify'], get(e['town'], e['id']), 'Quests#List_of_Special_Orders', True)), '</li>'))
        if truth(binary('>', get(e['need'], 'length'), 0)):
            put(e['meta'], 'hasDetails', True)
            e.set('output', binary('+', e['output'], binary('+', binary('+', binary('+', binary('+', '<div class="', get(e['meta'], 'anchor')), '_details '), get(e['meta'], 'det_class')), '">')))
            e.set('output', binary('+', e['output'], binary('+', binary('+', '<span class="need">Left to complete:<ol>', call(get(call(get(e['need'], 'sort')), 'join'), '')), '</ol></span></div>')))
    e.set('output', binary('+', binary('+', call(e['getSectionHeader'], e['saveInfo'], e['title'], e['anchor'], get(e['meta'], 'hasDetails'), e['version']), e['output']), call(e['getSectionFooter'])))
    return e['output']
    return U


def callback_199(parent, this, args):
    # Upstream checkup: 4549
    e = Env(parent)
    e.declare([])
    e.local['arguments'] = Array(args)
    e.set('id', call(get(call(e['$'], this), 'text')))
    if truth(call(get(e['trackerAllAtOnce'], 'hasOwnProperty'), e['id'])):
        put(e['found'], e['id'], get(get(e['trackerAllAtOnce'], e['id']), 'num'))
        e.set('found_count', binary('+', e['found_count'], get(get(e['trackerAllAtOnce'], e['id']), 'num')))
    return U


def callback_200(parent, this, args):
    # Upstream checkup: 4557
    e = Env(parent)
    e.declare(['n'])
    e.local['arguments'] = Array(args)
    e.set('id', call(get(call(get(call(e['$'], this), 'find'), 'key > string'), 'text')))
    e.set('num', call(e['Number'], call(get(call(get(call(e['$'], this), 'find'), 'value > int'), 'text'))))
    if truth((binary('>', e['num'], 0) if truth(_logic201 := call(get(e['trackerLimited'], 'hasOwnProperty'), e['id'])) else _logic201)):
        e.set('n', call(get(e['Math'], 'min'), e['num'], get(get(e['trackerLimited'], e['id']), 'num')))
        put(e['found'], e['id'], e['n'])
        e.set('found_count', binary('+', e['found_count'], e['n']))
    return U


def parseWalnuts_198(parent, this, args):
    # Upstream checkup: 4438
    e = Env(parent)
    e.declare(['anchor', 'count', 'det_class', 'extra', 'forceShowSpoilers', 'found', 'found_count', 'game_count', 'gcc', 'i', 'id', 'intro', 'keys', 'meta', 'need', 'num', 'output', 'parrotUsed', 'places', 'playerOutput', 'pt_pct', 'sum_class', 'title', 'trackerAllAtOnce', 'trackerExtra', 'trackerLimited', 'umid', 'val', 'version', 'x'])
    e.local['arguments'] = Array(args)
    e.local['xmlDoc'] = (args[0] if len(args) > 0 and args[0] is not U else U)
    e.local['saveInfo'] = (args[1] if len(args) > 1 and args[1] is not U else U)
    e.set('title', 'Golden Walnuts')
    e.set('anchor', call(e['makeAnchor'], e['title']))
    e.set('version', '1.5')
    e.set('sum_class', call(e['getSummaryClass'], e['saveInfo'], e['version']))
    e.set('det_class', call(e['getDetailsClass'], e['saveInfo'], e['version']))
    e.set('output', '')
    e.set('playerOutput', '')
    e.set('meta', Obj({'hasDetails': False, 'anchor': e['anchor'], 'sum_class': e['sum_class'], 'det_class': e['det_class']}))
    e.set('count', 0)
    e.set('found_count', 0)
    e.set('game_count', call(e['Number'], call(get(call(get(call(e['$'], e['xmlDoc']), 'find'), 'goldenWalnutsFound'), 'text'))))
    e.set('parrotUsed', binary('===', call(get(call(get(call(e['$'], e['xmlDoc']), 'find'), 'activatedGoldenParrot'), 'text')), 'true'))
    e.set('found', Obj({}))
    e.set('need', Obj({}))
    e.set('umid', 'global')
    e.set('pt_pct', '')
    e.set('trackerAllAtOnce', table(21))
    e.set('trackerExtra', Obj({'GoldenCoconut': Obj({'num': 1, 'name': 'Break a Golden Coconut', 'hint': ''})}))
    e.set('trackerLimited', table(22))
    if truth(binary('<', call(e['compareSemVer'], get(e['saveInfo'], 'version'), e['version']), 0)):
        return ''
    e.set('gcc', call(get(call(get(call(e['$'], e['xmlDoc']), 'find'), 'SaveGame > goldenCoconutCracked'), 'text')))
    if truth(binary('===', e['gcc'], 'true')):
        put(e['found'], 'GoldenCoconut', 1)
        update_env(e, 'found_count', 1, False)
    call(get(call(get(call(e['$'], e['xmlDoc']), 'find'), 'collectedNutTracker > string'), 'each'), Fn(callback_199, e))
    call(get(call(get(call(e['$'], e['xmlDoc']), 'find'), 'limitedNutDrops > item'), 'each'), Fn(callback_200, e))
    for _key202 in keys(e['trackerAllAtOnce']):
        e.set('id', _key202)
        if truth(call(get(e['trackerAllAtOnce'], 'hasOwnProperty'), e['id'])):
            e.set('count', binary('+', e['count'], get(get(e['trackerAllAtOnce'], e['id']), 'num')))
            if truth(unary('!', call(get(e['found'], 'hasOwnProperty'), e['id']))):
                put(e['need'], e['id'], get(get(e['trackerAllAtOnce'], e['id']), 'num'))
    for _key203 in keys(e['trackerExtra']):
        e.set('id', _key203)
        if truth(call(get(e['trackerExtra'], 'hasOwnProperty'), e['id'])):
            e.set('count', binary('+', e['count'], get(get(e['trackerExtra'], e['id']), 'num')))
            if truth(unary('!', call(get(e['found'], 'hasOwnProperty'), e['id']))):
                put(e['need'], e['id'], get(get(e['trackerExtra'], e['id']), 'num'))
    for _key204 in keys(e['trackerLimited']):
        e.set('id', _key204)
        if truth(call(get(e['trackerLimited'], 'hasOwnProperty'), e['id'])):
            e.set('count', binary('+', e['count'], get(get(e['trackerLimited'], e['id']), 'num')))
            if truth(call(get(e['found'], 'hasOwnProperty'), e['id'])):
                if truth(binary('<', get(e['found'], e['id']), get(get(e['trackerLimited'], e['id']), 'num'))):
                    put(e['need'], e['id'], binary('-', get(get(e['trackerLimited'], e['id']), 'num'), get(e['found'], e['id'])))
            else:
                put(e['need'], e['id'], get(get(e['trackerLimited'], e['id']), 'num'))
    put(get(get(e['saveInfo'], 'perfectionTracker'), e['umid']), 'Walnuts', Obj({'count': e['game_count'], 'total': e['count']}))
    if truth(binary('>=', call(e['compareSemVer'], get(e['saveInfo'], 'version'), '1.5'), 0)):
        e.set('x', call(get(e['Math'], 'min'), 100, binary('/', binary('*', 100, e['game_count']), e['count'])))
        e.set('places', (1 if truth(binary('<', e['x'], 100)) else 0))
        e.set('x', call(get(e['x'], 'toFixed'), e['places']))
        e.set('pt_pct', call(e['getPTLink'], binary('+', e['x'], '%')))
    e.set('output', binary('+', e['output'], binary('+', binary('+', binary('+', binary('+', '<div class="', get(e['meta'], 'anchor')), '_summary '), get(e['meta'], 'sum_class')), '">')))
    if truth(binary('>', get(e['saveInfo'], 'numPlayers'), 1)):
        e.set('intro', binary('+', binary('+', 'Inhabitants of ', get(e['saveInfo'], 'farmName')), ' Farm have'))
    else:
        e.set('intro', binary('+', get(get(e['saveInfo'], 'players'), get(e['saveInfo'], 'farmerId')), ' has'))
    e.set('output', binary('+', e['output'], binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', '<span class="result">', e['intro']), ' found '), e['game_count']), ' of '), e['count']), ' golden walnuts.'), e['pt_pct']), '</span>')))
    if truth(binary('!==', e['found_count'], e['game_count'])):
        e.set('output', binary('+', e['output'], binary('+', binary('+', binary('+', binary('+', '<br /><span class="result warn">Warning: Save lists a count of ', e['game_count']), " but we've found markers for "), e['found_count']), '</span>')))
    if truth(binary('<', e['game_count'], e['count'])):
        e.set('output', binary('+', e['output'], binary('+', binary('+', binary('+', binary('+', '<br/><span class="result">The ', call(e['wikify'], 'Golden Parrot', 'Golden_Walnut#Golden_Joja_Parrot')), ' will charge '), call(e['addCommas'], binary('*', 10000, binary('-', e['count'], e['game_count'])))), 'g to collect the rest.</span>')))
    else:
        e.set('output', binary('+', e['output'], binary('+', binary('+', binary('+', '<br/><span class="result">The ', call(e['wikify'], 'Golden Parrot', 'Golden_Walnut#Golden_Joja_Parrot')), (' was' if truth(e['parrotUsed']) else ' was not')), ' used to finish the collection.</span>')))
    e.set('output', binary('+', e['output'], '<ul class="ach_list"><li>'))
    e.set('output', binary('+', e['output'], (call(e['getMilestoneString'], "Collect enough walnuts (10) to earn Leo's trust.", 1) if truth(binary('>=', e['game_count'], 10)) else binary('+', binary('+', call(e['getMilestoneString'], "Collect enough walnuts (10) to earn Leo's trust.", 0), binary('-', 10, e['game_count'])), ' more'))))
    e.set('output', binary('+', e['output'], '</li>\n<li>'))
    e.set('output', binary('+', e['output'], (call(e['getMilestoneString'], 'Collect enough walnuts (101) to access the secret room.', 1) if truth(binary('>=', e['game_count'], 101)) else binary('+', binary('+', call(e['getMilestoneString'], 'Collect enough walnuts (101) to access the secret room', 0), binary('-', 101, e['game_count'])), ' more'))))
    e.set('output', binary('+', e['output'], '</li>\n<li>'))
    e.set('output', binary('+', e['output'], '</li></ul></div>'))
    if truth(binary('<', e['found_count'], e['count'])):
        put(e['meta'], 'hasDetails', True)
        e.set('output', binary('+', e['output'], binary('+', binary('+', binary('+', binary('+', '<div class="', get(e['meta'], 'anchor')), '_details '), get(e['meta'], 'det_class')), '">')))
        e.set('output', binary('+', e['output'], '<span class="need">Left to find:<ol>'))
        e.set('val', 0)
        e.set('keys', call(get(e['Object'], 'keys'), e['need']))
        e.set('forceShowSpoilers', False)
        for _key205 in keys(e['keys']):
            e.set('i', _key205)
            e.set('id', get(e['keys'], e['i']))
            e.set('val', binary('+', e['val'], get(e['need'], e['id'])))
            e.set('output', binary('+', e['output'], binary('+', binary('+', '<li value="', e['val']), '">')))
            e.set('extra', '')
            if truth(binary('>', get(e['need'], e['id']), 1)):
                e.set('extra', binary('+', binary('+', ' -- ', get(e['need'], e['id'])), ' walnuts'))
            if truth(call(get(e['trackerAllAtOnce'], 'hasOwnProperty'), e['id'])):
                e.set('output', binary('+', e['output'], binary('+', get(get(e['trackerAllAtOnce'], e['id']), 'name'), e['extra'])))
                if truth(binary('!==', get(get(e['trackerAllAtOnce'], e['id']), 'hint'), '')):
                    if truth(e['forceShowSpoilers']):
                        e.set('output', binary('+', e['output'], binary('+', binary('+', ' -- <span class="note">', get(get(e['trackerAllAtOnce'], e['id']), 'hint')), '</span>')))
                    else:
                        e.set('output', binary('+', e['output'], binary('+', binary('+', ' (<span class="note" data-tooltip="', get(get(e['trackerAllAtOnce'], e['id']), 'hint')), '">Hover for spoilers</span>)')))
                e.set('output', binary('+', e['output'], '</li>'))
            else:
                if truth(call(get(e['trackerExtra'], 'hasOwnProperty'), e['id'])):
                    e.set('output', binary('+', e['output'], binary('+', get(get(e['trackerExtra'], e['id']), 'name'), e['extra'])))
                    if truth(binary('!==', get(get(e['trackerExtra'], e['id']), 'hint'), '')):
                        if truth(e['forceShowSpoilers']):
                            e.set('output', binary('+', e['output'], binary('+', binary('+', ' -- <span class="note">', get(get(e['trackerExtra'], e['id']), 'hint')), '</span>')))
                        else:
                            e.set('output', binary('+', e['output'], binary('+', binary('+', ' (<span class="note" data-tooltip="', get(get(e['trackerExtra'], e['id']), 'hint')), '">Hover for spoilers</span>)')))
                    e.set('output', binary('+', e['output'], '</li>'))
                else:
                    if truth(call(get(e['trackerLimited'], 'hasOwnProperty'), e['id'])):
                        e.set('output', binary('+', e['output'], binary('+', get(get(e['trackerLimited'], e['id']), 'name'), e['extra'])))
                        if truth(binary('!==', get(get(e['trackerLimited'], e['id']), 'hint'), '')):
                            if truth(e['forceShowSpoilers']):
                                e.set('output', binary('+', e['output'], binary('+', binary('+', ' -- <span class="note">', get(get(e['trackerLimited'], e['id']), 'hint')), '</span>')))
                            else:
                                e.set('output', binary('+', e['output'], binary('+', binary('+', ' (<span class="note" data-tooltip="', get(get(e['trackerLimited'], e['id']), 'hint')), '">Hover for spoilers</span>)')))
                        e.set('output', binary('+', e['output'], '</li>'))
                    else:
                        call(get(e['console'], 'log'), binary('+', 'Walnut tracking found unknown id: ', e['id']))
        e.set('output', binary('+', e['output'], '</ol></span></div>'))
    e.set('output', binary('+', binary('+', call(e['getSectionHeader'], e['saveInfo'], e['title'], e['anchor'], get(e['meta'], 'hasDetails'), e['version']), e['output']), call(e['getSectionFooter'])))
    return e['output']
    return U


def callback_207(parent, this, args):
    # Upstream checkup: 4730
    e = Env(parent)
    e.declare([])
    e.local['arguments'] = Array(args)
    e.local['id'] = (args[0] if len(args) > 0 and args[0] is not U else U)
    if truth((call(get(get(get(get(e['saveInfo'], 'data'), get(e['saveInfo'], 'farmerId')), 'mailReceived'), 'hasOwnProperty'), e['id']) if truth(_logic208 := call(get(e['upgrades'], 'hasOwnProperty'), e['id'])) else _logic208)):
        put(e['bought'], e['id'], 1)
        update_env(e, 'bought_count', 1, False)
    else:
        put(e['need'], e['id'], get(get(e['upgrades'], e['id']), 'cost'))
        e.set('cost', binary('+', e['cost'], get(get(e['upgrades'], e['id']), 'cost')))
    return U


def parseIslandUpgrades_206(parent, this, args):
    # Upstream checkup: 4697
    e = Env(parent)
    e.declare(['anchor', 'bought', 'bought_count', 'cost', 'count', 'det_class', 'extra', 'i', 'id', 'intro', 'keys', 'meta', 'need', 'output', 'playerOutput', 'sum_class', 'title', 'upgrades', 'val', 'version'])
    e.local['arguments'] = Array(args)
    e.local['xmlDoc'] = (args[0] if len(args) > 0 and args[0] is not U else U)
    e.local['saveInfo'] = (args[1] if len(args) > 1 and args[1] is not U else U)
    e.set('title', 'Island Upgrades')
    e.set('anchor', call(e['makeAnchor'], e['title']))
    e.set('version', '1.5')
    e.set('sum_class', call(e['getSummaryClass'], e['saveInfo'], e['version']))
    e.set('det_class', call(e['getDetailsClass'], e['saveInfo'], e['version']))
    e.set('output', '')
    e.set('playerOutput', '')
    e.set('meta', Obj({'hasDetails': False, 'anchor': e['anchor'], 'sum_class': e['sum_class'], 'det_class': e['det_class']}))
    e.set('count', 0)
    e.set('bought_count', 0)
    e.set('bought', Obj({}))
    e.set('need', Obj({}))
    e.set('cost', 0)
    e.set('upgrades', table(23))
    if truth(binary('<', call(e['compareSemVer'], get(e['saveInfo'], 'version'), e['version']), 0)):
        return ''
    e.set('count', get(call(get(e['Object'], 'keys'), e['upgrades']), 'length'))
    call(get(call(get(e['Object'], 'keys'), e['upgrades']), 'forEach'), Fn(callback_207, e))
    e.set('output', binary('+', e['output'], binary('+', binary('+', binary('+', binary('+', '<div class="', get(e['meta'], 'anchor')), '_summary '), get(e['meta'], 'sum_class')), '">')))
    if truth(binary('>', get(e['saveInfo'], 'numPlayers'), 1)):
        e.set('intro', binary('+', binary('+', 'Inhabitants of ', get(e['saveInfo'], 'farmName')), ' Farm have'))
    else:
        e.set('intro', binary('+', get(get(e['saveInfo'], 'players'), get(e['saveInfo'], 'farmerId')), ' has'))
    e.set('output', binary('+', e['output'], binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', '<span class="result">', e['intro']), ' purchased '), e['bought_count']), ' of '), e['count']), ' Island Upgrades.</span><ul class="ach_list">\n')))
    e.set('output', binary('+', e['output'], '<li>'))
    e.set('output', binary('+', e['output'], (call(e['getMilestoneString'], 'Purchase all upgrades.', 1) if truth(binary('>=', e['bought_count'], e['count'])) else binary('+', binary('+', binary('+', binary('+', call(e['getMilestoneString'], 'Purchase all upgrades', 0), binary('-', e['count'], e['bought_count'])), ' more (costs '), e['cost']), ' walnuts)'))))
    e.set('output', binary('+', e['output'], '</li></ul></div>'))
    if truth(binary('<', e['bought_count'], e['count'])):
        put(e['meta'], 'hasDetails', True)
        e.set('output', binary('+', e['output'], binary('+', binary('+', binary('+', binary('+', '<div class="', get(e['meta'], 'anchor')), '_details '), get(e['meta'], 'det_class')), '">')))
        e.set('output', binary('+', e['output'], '<span class="need">Left to buy:<ol>'))
        e.set('val', 0)
        e.set('keys', call(get(e['Object'], 'keys'), e['need']))
        for _key209 in keys(e['keys']):
            e.set('i', _key209)
            e.set('id', get(e['keys'], e['i']))
            e.set('extra', '')
            if truth(binary('>', get(e['need'], e['id']), 1)):
                e.set('extra', binary('+', binary('+', ' -- costs ', get(e['need'], e['id'])), ' walnuts'))
            e.set('output', binary('+', e['output'], binary('+', binary('+', binary('+', '<li>', get(get(e['upgrades'], e['id']), 'name')), e['extra']), '</li>')))
        e.set('output', binary('+', e['output'], '</ol></span></div>'))
    e.set('output', binary('+', binary('+', call(e['getSectionHeader'], e['saveInfo'], e['title'], e['anchor'], get(e['meta'], 'hasDetails'), e['version']), e['output']), call(e['getSectionFooter'])))
    return e['output']
    return U


def callback_211(parent, this, args):
    # Upstream checkup: 4803
    e = Env(parent)
    e.declare([])
    e.local['arguments'] = Array(args)
    e.set('type', call(get(call(get(call(e['$'], this), 'children'), 'buildingType'), 'text')))
    if truth(call(get(get(get(e['saveInfo'], 'perfectionTracker'), 'global'), 'hasOwnProperty'), e['type'])):
        put(get(get(e['saveInfo'], 'perfectionTracker'), 'global'), e['type'], True)
    return U


def callback_213(parent, this, args):
    # Upstream checkup: 4823
    e = Env(parent)
    e.declare(['p'])
    e.local['arguments'] = Array(args)
    e.local['umid'] = (args[0] if len(args) > 0 and args[0] is not U else U)
    e.set('p', call(get(e['Math'], 'min'), binary('/', get(get(get(get(e['saveInfo'], 'perfectionTracker'), e['umid']), e['k']), 'count'), get(get(get(get(e['saveInfo'], 'perfectionTracker'), e['umid']), e['k']), 'total')), 1))
    if truth(binary('>', e['p'], get(e['pct'], e['k']))):
        put(e['pct'], e['k'], e['p'])
        put(e['best'], e['k'], get(get(e['saveInfo'], 'players'), e['umid']))
    return U


def callback_212(parent, this, args):
    # Upstream checkup: 4820
    e = Env(parent)
    e.declare([])
    e.local['arguments'] = Array(args)
    e.local['k'] = (args[0] if len(args) > 0 and args[0] is not U else U)
    put(e['pct'], e['k'], 0)
    put(e['best'], e['k'], '')
    call(get(call(get(e['Object'], 'keys'), get(e['saveInfo'], 'players')), 'forEach'), Fn(callback_213, e))
    return U


def callback_215(parent, this, args):
    # Upstream checkup: 4835
    e = Env(parent)
    e.declare([])
    e.local['arguments'] = Array(args)
    e.local['umid'] = (args[0] if len(args) > 0 and args[0] is not U else U)
    if truth((get(get(get(e['saveInfo'], 'perfectionTracker'), e['umid']), e['k']) if truth(_logic216 := unary('!', get(e['pct'], e['k']))) else _logic216)):
        put(e['pct'], e['k'], True)
        put(e['best'], e['k'], get(get(e['saveInfo'], 'players'), e['umid']))
    return U


def callback_214(parent, this, args):
    # Upstream checkup: 4832
    e = Env(parent)
    e.declare([])
    e.local['arguments'] = Array(args)
    e.local['k'] = (args[0] if len(args) > 0 and args[0] is not U else U)
    put(e['pct'], e['k'], False)
    put(e['best'], e['k'], '')
    call(get(call(get(e['Object'], 'keys'), get(e['saveInfo'], 'players')), 'forEach'), Fn(callback_215, e))
    return U


def parsePerfectionTracker_210(parent, this, args):
    # Upstream checkup: 4775
    e = Env(parent)
    e.declare(['adj_pct', 'anchor', 'bKeys', 'best', 'buildings', 'det_class', 'extra', 'left', 'meta', 'missingObelisks', 'need', 'numObelisks', 'output', 'pKeys', 'pct', 'places', 'playerOutput', 'pt_pct', 'sum_class', 'title', 'type', 'version', 'waivers'])
    e.local['arguments'] = Array(args)
    e.local['xmlDoc'] = (args[0] if len(args) > 0 and args[0] is not U else U)
    e.local['saveInfo'] = (args[1] if len(args) > 1 and args[1] is not U else U)
    e.set('title', 'Perfection Tracker')
    e.set('anchor', call(e['makeAnchor'], e['title']))
    e.set('version', '1.5')
    e.set('sum_class', call(e['getSummaryClass'], e['saveInfo'], e['version']))
    e.set('det_class', call(e['getDetailsClass'], e['saveInfo'], e['version']))
    e.set('output', '')
    e.set('playerOutput', '')
    e.set('meta', Obj({'hasDetails': False, 'anchor': e['anchor'], 'sum_class': e['sum_class'], 'det_class': e['det_class']}))
    e.set('buildings', call(get(call(e['$'], e['xmlDoc']), 'find'), binary('+', binary('+', 'locations > GameLocation[', get(e['saveInfo'], 'ns_prefix')), "\\:type='Farm'] > buildings")))
    e.set('pt_pct', 0)
    e.set('adj_pct', 0)
    e.set('waivers', (call(e['Number'], call(get(call(get(call(e['$'], e['xmlDoc']), 'find'), 'perfectionWaivers'), 'text'))) if truth(binary('>=', call(e['compareSemVer'], get(e['saveInfo'], 'version'), '1.6'), 0)) else 0))
    e.set('extra', (binary('+', binary('+', '(+', e['waivers']), ' Waivers)') if truth(binary('>', e['waivers'], 0)) else ''))
    e.set('places', 1)
    e.set('numObelisks', 0)
    e.set('missingObelisks', Array([]))
    e.set('pKeys', Array(['Shipping', 'Cooking', 'Crafting', 'Fishing', 'Great Friends', 'Skills']))
    e.set('bKeys', Array(['Monsters', 'Stardrops']))
    e.set('need', '')
    if truth(binary('<', call(e['compareSemVer'], get(e['saveInfo'], 'version'), e['version']), 0)):
        return ''
    call(get(call(get(call(e['$'], e['buildings']), 'children'), 'Building'), 'each'), Fn(callback_211, e))
    if truth(get(get(get(e['saveInfo'], 'perfectionTracker'), 'global'), 'Earth Obelisk')):
        update_env(e, 'numObelisks', 1, False)
    else:
        call(get(e['missingObelisks'], 'push'), call(e['wikify'], 'Earth', 'Earth Obelisk', 1))
    if truth(get(get(get(e['saveInfo'], 'perfectionTracker'), 'global'), 'Water Obelisk')):
        update_env(e, 'numObelisks', 1, False)
    else:
        call(get(e['missingObelisks'], 'push'), call(e['wikify'], 'Water', 'Water Obelisk', 1))
    if truth(get(get(get(e['saveInfo'], 'perfectionTracker'), 'global'), 'Desert Obelisk')):
        update_env(e, 'numObelisks', 1, False)
    else:
        call(get(e['missingObelisks'], 'push'), call(e['wikify'], 'Desert', 'Desert Obelisk', 1))
    if truth(get(get(get(e['saveInfo'], 'perfectionTracker'), 'global'), 'Island Obelisk')):
        update_env(e, 'numObelisks', 1, False)
    else:
        call(get(e['missingObelisks'], 'push'), call(e['wikify'], 'Island', 'Island Obelisk', 1))
    e.set('numObelisks', call(get(e['Math'], 'min'), e['numObelisks'], 4))
    e.set('pct', Obj({'Walnuts': call(get(e['Math'], 'min'), binary('/', get(get(get(get(e['saveInfo'], 'perfectionTracker'), 'global'), 'Walnuts'), 'count'), get(get(get(get(e['saveInfo'], 'perfectionTracker'), 'global'), 'Walnuts'), 'total')), 1)}))
    e.set('best', Obj({}))
    call(get(e['pKeys'], 'forEach'), Fn(callback_212, e))
    call(get(e['bKeys'], 'forEach'), Fn(callback_214, e))
    e.set('pt_pct', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', e['numObelisks'], (10 if truth(get(get(get(e['saveInfo'], 'perfectionTracker'), 'global'), 'Gold Clock')) else 0)), (10 if truth(get(e['pct'], 'Monsters')) else 0)), (10 if truth(get(e['pct'], 'Stardrops')) else 0)), binary('*', 15, get(e['pct'], 'Shipping'))), binary('*', 11, get(e['pct'], 'Great Friends'))), binary('*', 10, get(e['pct'], 'Cooking'))), binary('*', 10, get(e['pct'], 'Crafting'))), binary('*', 10, get(e['pct'], 'Fishing'))), binary('*', 5, get(e['pct'], 'Walnuts'))), binary('*', 5, get(e['pct'], 'Skills'))))
    0
    e.set('left', binary('-', binary('-', 100, e['pt_pct']), e['waivers']))
    e.set('adj_pct', call(get(e['Math'], 'min'), 100, binary('+', e['pt_pct'], e['waivers'])))
    e.set('adj_pct', call(get(e['adj_pct'], 'toFixed'), (1 if truth(binary('<', e['adj_pct'], 100)) else 0)))
    e.set('pt_pct', call(get(e['pt_pct'], 'toFixed'), (1 if truth(binary('<', e['pt_pct'], 100)) else 0)))
    e.set('left', call(get(e['left'], 'toFixed'), (1 if truth(binary('<', e['left'], 100)) else 0)))
    e.set('output', binary('+', binary('+', binary('+', binary('+', '<div class="', get(e['meta'], 'anchor')), '_summary '), get(e['meta'], 'sum_class')), '">'))
    e.set('output', binary('+', e['output'], binary('+', binary('+', binary('+', binary('+', binary('+', '<span class="result">', 'Inhabitants of '), get(e['saveInfo'], 'farmName')), ' Farm have earned '), e['adj_pct']), '% Total Perfection (details below).</span>')))
    e.set('output', binary('+', e['output'], binary('+', binary('+', binary('+', binary('+', '<br/><span class="result">Note that the Walnut Room display always rounds down and will show: ', call(get(e['Math'], 'floor'), e['pt_pct'])), '% '), e['extra']), '</span>')))
    e.set('output', binary('+', e['output'], '<ul class="ach_list"><li>'))
    e.set('output', binary('+', e['output'], (call(e['getMilestoneString'], '100% Completion', 1) if truth(binary('>=', e['pt_pct'], 100)) else binary('+', binary('+', call(e['getMilestoneString'], '100% Completion', 0), e['left']), '% more'))))
    e.set('output', binary('+', e['output'], '</li></ul></div>'))
    put(e['meta'], 'hasDetails', True)
    e.set('output', binary('+', e['output'], binary('+', binary('+', binary('+', binary('+', '<div class="', get(e['meta'], 'anchor')), '_details '), get(e['meta'], 'det_class')), '">')))
    e.set('output', binary('+', e['output'], '<span class="result">Percentage Breakdown</span>'))
    e.set('output', binary('+', e['output'], '<ul class="ach_list"><li>'))
    e.set('output', binary('+', e['output'], (call(e['getPerfectionPctString'], get(e['pct'], 'Shipping'), 15, 'Produce &amp; Forage Shipped', 1, get(e['best'], 'Shipping')) if truth(binary('>=', get(e['pct'], 'Shipping'), 1)) else binary('+', call(e['getPerfectionPctString'], get(e['pct'], 'Shipping'), 15, 'Produce &amp; Forage Shipped', 0, get(e['best'], 'Shipping')), ' -- <a href="#sec_Basic_Shipping">see above for needs</a>'))))
    e.set('output', binary('+', e['output'], '</li><li>'))
    e.set('output', binary('+', e['output'], (call(e['getPerfectionNumString'], e['numObelisks'], 4, 'Obelisks on Farm', 1) if truth(binary('==', e['numObelisks'], 4)) else binary('+', binary('+', call(e['getPerfectionNumString'], e['numObelisks'], 4, 'Obelisks on Farm', 0), ' -- need '), call(get(e['missingObelisks'], 'join'), ', ')))))
    e.set('output', binary('+', e['output'], '</li><li>'))
    e.set('output', binary('+', e['output'], binary('+', call(e['getPerfectionBoolString'], 10, 'Golden Clock on Farm', get(get(get(e['saveInfo'], 'perfectionTracker'), 'global'), 'Gold Clock')), ('' if truth(get(get(get(e['saveInfo'], 'perfectionTracker'), 'global'), 'Gold Clock')) else binary('+', ' -- need to build a ', call(e['wikify'], 'Gold Clock'))))))
    e.set('output', binary('+', e['output'], '</li><li>'))
    e.set('output', binary('+', e['output'], binary('+', call(e['getPerfectionBoolString'], 10, 'Monster Slayer Hero (all slayer goals)', get(e['pct'], 'Monsters'), get(e['best'], 'Monsters')), ('' if truth(get(e['pct'], 'Monsters')) else ' -- <a href="#sec_Monster_Hunting">see above for needs</a>'))))
    e.set('output', binary('+', e['output'], '</li><li>'))
    e.set('output', binary('+', e['output'], (call(e['getPerfectionPctString'], get(e['pct'], 'Great Friends'), 11, 'Great Friends (maxing all relationships)', 1, get(e['best'], 'Great Friends')) if truth(binary('>=', get(e['pct'], 'Great Friends'), 1)) else binary('+', call(e['getPerfectionPctString'], get(e['pct'], 'Great Friends'), 11, 'Great Friends (maxing all relationships)', 0, get(e['best'], 'Great Friends')), ' -- <a href="#sec_Social">see above for needs</a>'))))
    e.set('output', binary('+', e['output'], '</li><li>'))
    e.set('output', binary('+', e['output'], (call(e['getPerfectionPctNumString'], get(e['pct'], 'Skills'), 5, 25, 'Farmer Level (max all skills)', 1, get(e['best'], 'Skills')) if truth(binary('>=', get(e['pct'], 'Skills'), 1)) else binary('+', call(e['getPerfectionPctNumString'], get(e['pct'], 'Skills'), 5, 25, 'Farmer Level (max all skills)', 0, get(e['best'], 'Skills')), ' -- <a href="#sec_Skills">see above for needs</a>'))))
    e.set('output', binary('+', e['output'], '</li><li>'))
    e.set('output', binary('+', e['output'], binary('+', call(e['getPerfectionBoolString'], 10, 'Found All Stardrops', get(e['pct'], 'Stardrops'), get(e['best'], 'Stardrops')), ('' if truth(get(e['pct'], 'Stardrops')) else ' -- <a href="#sec_Stardrops">see above for needs</a>'))))
    e.set('output', binary('+', e['output'], '</li><li>'))
    e.set('output', binary('+', e['output'], (call(e['getPerfectionPctString'], get(e['pct'], 'Cooking'), 10, 'Cooking Recipes Made', 1, get(e['best'], 'Cooking')) if truth(binary('>=', get(e['pct'], 'Cooking'), 1)) else binary('+', call(e['getPerfectionPctString'], get(e['pct'], 'Cooking'), 10, 'Cooking Recipes Made', 0, get(e['best'], 'Cooking')), ' -- <a href="#sec_Cooking">see above for needs</a>'))))
    e.set('output', binary('+', e['output'], '</li><li>'))
    e.set('output', binary('+', e['output'], (call(e['getPerfectionPctString'], get(e['pct'], 'Crafting'), 10, 'Crafting Recipes Made', 1, get(e['best'], 'Crafting')) if truth(binary('>=', get(e['pct'], 'Crafting'), 1)) else binary('+', call(e['getPerfectionPctString'], get(e['pct'], 'Crafting'), 10, 'Crafting Recipes Made', 0, get(e['best'], 'Crafting')), ' -- <a href="#sec_Crafting">see above for needs</a>'))))
    e.set('output', binary('+', e['output'], '</li><li>'))
    e.set('output', binary('+', e['output'], (call(e['getPerfectionPctString'], get(e['pct'], 'Fishing'), 10, 'Fish Caught', 1, get(e['best'], 'Fishing')) if truth(binary('>=', get(e['pct'], 'Fishing'), 1)) else binary('+', call(e['getPerfectionPctString'], get(e['pct'], 'Fishing'), 10, 'Fish Caught', 0, get(e['best'], 'Fishing')), ' -- <a href="#sec_Fishing">see above for needs</a>'))))
    e.set('output', binary('+', e['output'], '</li><li>'))
    e.set('output', binary('+', e['output'], (call(e['getPerfectionPctNumString'], get(e['pct'], 'Walnuts'), 5, 130, 'Golden Walnuts Found', 1) if truth(binary('>=', get(e['pct'], 'Walnuts'), 1)) else binary('+', call(e['getPerfectionPctNumString'], get(e['pct'], 'Walnuts'), 5, 130, 'Golden Walnuts Found', 0), ' -- <a href="#sec_Golden_Walnuts">see above for needs</a>'))))
    if truth(binary('>', e['waivers'], 0)):
        e.set('output', binary('+', e['output'], binary('+', binary('+', binary('+', binary('+', '</li><li><span class="pt_yes"><span class="pts">', e['waivers']), '%</span> from purchase of '), e['waivers']), ' Perfection Waivers</span>')))
    e.set('output', binary('+', e['output'], '</li></ul></div>'))
    e.set('output', binary('+', binary('+', call(e['getSectionHeader'], e['saveInfo'], e['title'], e['anchor'], get(e['meta'], 'hasDetails'), e['version']), e['output']), call(e['getSectionFooter'])))
    return e['output']
    return U


def parsePlayerPerfection_217(parent, this, args):
    # Upstream checkup: 4905
    e = Env(parent)
    e.declare(['farmer', 'left', 'missingObelisks', 'need', 'numObelisks', 'output', 'pct', 'places', 'pt_pct', 'table', 'umid'])
    e.local['arguments'] = Array(args)
    e.local['player'] = (args[0] if len(args) > 0 and args[0] is not U else U)
    e.local['saveInfo'] = (args[1] if len(args) > 1 and args[1] is not U else U)
    e.local['meta'] = (args[2] if len(args) > 2 and args[2] is not U else U)
    e.set('output', '')
    e.set('table', Array([]))
    e.set('farmer', call(get(call(get(call(e['$'], e['player']), 'children'), 'name'), 'html')))
    e.set('umid', call(get(call(get(call(e['$'], e['player']), 'children'), 'UniqueMultiplayerID'), 'text')))
    e.set('pt_pct', 0)
    e.set('places', 1)
    e.set('numObelisks', 0)
    e.set('missingObelisks', Array([]))
    e.set('need', '')
    if truth(get(get(get(e['saveInfo'], 'perfectionTracker'), 'global'), 'Earth Obelisk')):
        update_env(e, 'numObelisks', 1, False)
    else:
        call(get(e['missingObelisks'], 'push'), 'Earth')
    if truth(get(get(get(e['saveInfo'], 'perfectionTracker'), 'global'), 'Water Obelisk')):
        update_env(e, 'numObelisks', 1, False)
    else:
        call(get(e['missingObelisks'], 'push'), 'Water')
    if truth(get(get(get(e['saveInfo'], 'perfectionTracker'), 'global'), 'Desert Obelisk')):
        update_env(e, 'numObelisks', 1, False)
    else:
        call(get(e['missingObelisks'], 'push'), 'Desert')
    if truth(get(get(get(e['saveInfo'], 'perfectionTracker'), 'global'), 'Island Obelisk')):
        update_env(e, 'numObelisks', 1, False)
    else:
        call(get(e['missingObelisks'], 'push'), 'Island')
    e.set('pct', Obj({'Walnuts': call(get(e['Math'], 'min'), binary('/', get(get(get(get(e['saveInfo'], 'perfectionTracker'), 'global'), 'Walnuts'), 'count'), get(get(get(get(e['saveInfo'], 'perfectionTracker'), 'global'), 'Walnuts'), 'total')), 1), 'Shipping': binary('/', get(get(get(get(e['saveInfo'], 'perfectionTracker'), e['umid']), 'Shipping'), 'count'), get(get(get(get(e['saveInfo'], 'perfectionTracker'), e['umid']), 'Shipping'), 'total')), 'Cooking': binary('/', get(get(get(get(e['saveInfo'], 'perfectionTracker'), e['umid']), 'Cooking'), 'count'), get(get(get(get(e['saveInfo'], 'perfectionTracker'), e['umid']), 'Cooking'), 'total')), 'Crafting': binary('/', get(get(get(get(e['saveInfo'], 'perfectionTracker'), e['umid']), 'Crafting'), 'count'), get(get(get(get(e['saveInfo'], 'perfectionTracker'), e['umid']), 'Crafting'), 'total')), 'Fishing': binary('/', get(get(get(get(e['saveInfo'], 'perfectionTracker'), e['umid']), 'Fishing'), 'count'), get(get(get(get(e['saveInfo'], 'perfectionTracker'), e['umid']), 'Fishing'), 'total')), 'Great Friends': binary('/', get(get(get(get(e['saveInfo'], 'perfectionTracker'), e['umid']), 'Great Friends'), 'count'), get(get(get(get(e['saveInfo'], 'perfectionTracker'), e['umid']), 'Great Friends'), 'total')), 'Skills': call(get(e['Math'], 'min'), binary('/', get(get(get(get(e['saveInfo'], 'perfectionTracker'), e['umid']), 'Skills'), 'count'), get(get(get(get(e['saveInfo'], 'perfectionTracker'), e['umid']), 'Skills'), 'total')), 1)}))
    e.set('numObelisks', call(get(e['Math'], 'min'), e['numObelisks'], 4))
    e.set('pt_pct', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', e['numObelisks'], (10 if truth(get(get(get(e['saveInfo'], 'perfectionTracker'), 'global'), 'Gold Clock')) else 0)), (10 if truth(get(get(get(e['saveInfo'], 'perfectionTracker'), e['umid']), 'Monsters')) else 0)), (10 if truth(get(get(get(e['saveInfo'], 'perfectionTracker'), e['umid']), 'Stardrops')) else 0)), binary('*', 15, get(e['pct'], 'Shipping'))), binary('*', 11, get(e['pct'], 'Great Friends'))), binary('*', 10, get(e['pct'], 'Cooking'))), binary('*', 10, get(e['pct'], 'Crafting'))), binary('*', 10, get(e['pct'], 'Fishing'))), binary('*', 5, get(e['pct'], 'Walnuts'))), binary('*', 5, get(e['pct'], 'Skills'))))
    0
    e.set('pt_pct', call(get(e['pt_pct'], 'toFixed'), (1 if truth(binary('<', e['pt_pct'], 100)) else 0)))
    e.set('left', binary('-', 100, e['pt_pct']))
    e.set('left', call(get(e['left'], 'toFixed'), (1 if truth(binary('<', e['left'], 100)) else 0)))
    e.set('output', binary('+', binary('+', binary('+', binary('+', '<div class="', get(e['meta'], 'anchor')), '_summary '), get(e['meta'], 'sum_class')), '">'))
    e.set('output', binary('+', e['output'], binary('+', binary('+', binary('+', binary('+', '<span class="result">', e['farmer']), ' has '), e['pt_pct']), '% Total Completion (details below).</span>')))
    e.set('output', binary('+', e['output'], '<ul class="ach_list"><li>'))
    e.set('output', binary('+', e['output'], (call(e['getMilestoneString'], '100% Completion', 1) if truth(binary('>=', e['pt_pct'], 100)) else binary('+', binary('+', call(e['getMilestoneString'], '100% Completion', 0), e['left']), '% more'))))
    e.set('output', binary('+', e['output'], '</li></ul></div>'))
    put(e['meta'], 'hasDetails', True)
    e.set('output', binary('+', e['output'], binary('+', binary('+', binary('+', binary('+', '<div class="', get(e['meta'], 'anchor')), '_details '), get(e['meta'], 'det_class')), '">')))
    e.set('output', binary('+', e['output'], '<span class="result">Percentage Breakdown</span>'))
    e.set('output', binary('+', e['output'], '<ul class="ach_list"><li>'))
    e.set('output', binary('+', e['output'], (call(e['getPerfectionPctString'], get(e['pct'], 'Shipping'), 15, 'Produce &amp; Forage Shipped', 1) if truth(binary('>=', get(e['pct'], 'Shipping'), 1)) else binary('+', call(e['getPerfectionPctString'], get(e['pct'], 'Shipping'), 15, 'Produce &amp; Forage Shipped', 0), ' -- <a href="#sec_Basic_Shipping">see above for needs</a>'))))
    e.set('output', binary('+', e['output'], '</li><li>'))
    e.set('output', binary('+', e['output'], (call(e['getPerfectionNumString'], e['numObelisks'], 4, 'Obelisks on Farm', 1) if truth(binary('==', e['numObelisks'], 4)) else binary('+', binary('+', call(e['getPerfectionNumString'], e['numObelisks'], 4, 'Obelisks on Farm', 0), ' -- need '), call(get(e['missingObelisks'], 'join'), ', ')))))
    e.set('output', binary('+', e['output'], '</li><li>'))
    e.set('output', binary('+', e['output'], binary('+', call(e['getPerfectionBoolString'], 10, 'Golden Clock on Farm', get(get(get(e['saveInfo'], 'perfectionTracker'), 'global'), 'Gold Clock')), ('' if truth(get(get(get(e['saveInfo'], 'perfectionTracker'), 'global'), 'Gold Clock')) else binary('+', ' -- need to build a ', call(e['wikify'], 'Gold Clock'))))))
    e.set('output', binary('+', e['output'], '</li><li>'))
    e.set('output', binary('+', e['output'], binary('+', call(e['getPerfectionBoolString'], 10, 'Monster Slayer Hero (all slayer goals)', get(get(get(e['saveInfo'], 'perfectionTracker'), e['umid']), 'Monsters')), ('' if truth(get(get(get(e['saveInfo'], 'perfectionTracker'), e['umid']), 'Monsters')) else ' -- <a href="#sec_Monster_Hunting">see above for needs</a>'))))
    e.set('output', binary('+', e['output'], '</li><li>'))
    e.set('output', binary('+', e['output'], (call(e['getPerfectionPctString'], get(e['pct'], 'Great Friends'), 11, 'Great Friends (maxing all relationships)', 1) if truth(binary('>=', get(e['pct'], 'Great Friends'), 1)) else binary('+', call(e['getPerfectionPctString'], get(e['pct'], 'Great Friends'), 11, 'Great Friends (maxing all relationships)', 0), ' -- <a href="#sec_Social">see above for needs</a>'))))
    e.set('output', binary('+', e['output'], '</li><li>'))
    e.set('output', binary('+', e['output'], (call(e['getPerfectionPctNumString'], get(e['pct'], 'Skills'), 5, 25, 'Farmer Level (max all skills)', 1) if truth(binary('>=', get(e['pct'], 'Skills'), 1)) else binary('+', call(e['getPerfectionPctNumString'], get(e['pct'], 'Skills'), 5, 25, 'Farmer Level (max all skills)', 0), ' -- <a href="#sec_Skills">see above for needs</a>'))))
    e.set('output', binary('+', e['output'], '</li><li>'))
    e.set('output', binary('+', e['output'], binary('+', call(e['getPerfectionBoolString'], 10, 'Found All Stardrops', get(get(get(e['saveInfo'], 'perfectionTracker'), e['umid']), 'Stardrops')), ('' if truth(get(get(get(e['saveInfo'], 'perfectionTracker'), e['umid']), 'Stardrops')) else ' -- <a href="#sec_Stardrops">see above for needs</a>'))))
    e.set('output', binary('+', e['output'], '</li><li>'))
    e.set('output', binary('+', e['output'], (call(e['getPerfectionPctString'], get(e['pct'], 'Cooking'), 10, 'Cooking Recipes Made', 1) if truth(binary('>=', get(e['pct'], 'Cooking'), 1)) else binary('+', call(e['getPerfectionPctString'], get(e['pct'], 'Cooking'), 10, 'Cooking Recipes Made', 0), ' -- <a href="#sec_Cooking">see above for needs</a>'))))
    e.set('output', binary('+', e['output'], '</li><li>'))
    e.set('output', binary('+', e['output'], (call(e['getPerfectionPctString'], get(e['pct'], 'Crafting'), 10, 'Crafting Recipes Made', 1) if truth(binary('>=', get(e['pct'], 'Crafting'), 1)) else binary('+', call(e['getPerfectionPctString'], get(e['pct'], 'Crafting'), 10, 'Crafting Recipes Made', 0), ' -- <a href="#sec_Crafting">see above for needs</a>'))))
    e.set('output', binary('+', e['output'], '</li><li>'))
    e.set('output', binary('+', e['output'], (call(e['getPerfectionPctString'], get(e['pct'], 'Fishing'), 10, 'Fish Caught', 1) if truth(binary('>=', get(e['pct'], 'Fishing'), 1)) else binary('+', call(e['getPerfectionPctString'], get(e['pct'], 'Fishing'), 10, 'Fish Caught', 0), ' -- <a href="#sec_Fishing">see above for needs</a>'))))
    e.set('output', binary('+', e['output'], '</li><li>'))
    e.set('output', binary('+', e['output'], (call(e['getPerfectionPctNumString'], get(e['pct'], 'Walnuts'), 5, 130, 'Golden Walnuts Found', 1) if truth(binary('>=', get(e['pct'], 'Walnuts'), 1)) else binary('+', call(e['getPerfectionPctNumString'], get(e['pct'], 'Walnuts'), 5, 130, 'Golden Walnuts Found', 0), ' -- <a href="#sec_Golden_Walnuts">see above for needs</a>'))))
    e.set('output', binary('+', e['output'], '</li></ul></div>'))
    call(get(e['table'], 'push'), e['output'])
    return e['table']
    return U


def parsePowers_218(parent, this, args):
    # Upstream checkup: 4987
    e = Env(parent)
    e.declare(['anchor', 'det_class', 'meta', 'output', 'playerOutput', 'sum_class', 'table', 'title', 'version'])
    e.local['arguments'] = Array(args)
    e.local['xmlDoc'] = (args[0] if len(args) > 0 and args[0] is not U else U)
    e.local['saveInfo'] = (args[1] if len(args) > 1 and args[1] is not U else U)
    e.set('title', 'Books, Special Items &amp; Powers')
    e.set('anchor', call(e['makeAnchor'], e['title']))
    e.set('version', '1.6')
    e.set('sum_class', call(e['getSummaryClass'], e['saveInfo'], e['version']))
    e.set('det_class', call(e['getDetailsClass'], e['saveInfo'], e['version']))
    e.set('output', '')
    e.set('playerOutput', '')
    e.set('meta', Obj({'hasDetails': False, 'anchor': e['anchor'], 'sum_class': e['sum_class'], 'det_class': e['det_class']}))
    e.set('table', Array([]))
    (put(e['meta'], 'bookpowers', table(24)), put(e['meta'], 'otherpowers', table(25)), put(e['meta'], 'translate', table(26)), put(e['meta'], 'query', Obj({'PLAYER_HAS_SEEN_EVENT': 'eventsSeen', 'PLAYER_STAT': 'stats', 'PLAYER_HAS_FLAG': 'mailReceived'})))[-1]
    if truth(binary('<', call(e['compareSemVer'], get(e['saveInfo'], 'version'), e['version']), 0)):
        return ''
    put(e['table'], 0, call(e['parsePlayerPowers'], call(get(call(e['$'], e['xmlDoc']), 'find'), 'SaveGame > player'), e['saveInfo'], e['meta']))
    call(e['parseFarmhands'], e['xmlDoc'], e['saveInfo'], e['table'], e['parsePlayerPowers'], e['meta'])
    e.set('playerOutput', binary('+', e['playerOutput'], call(e['printTranspose'], e['table'])))
    e.set('output', binary('+', binary('+', call(e['getSectionHeader'], e['saveInfo'], e['title'], e['anchor'], get(e['meta'], 'hasDetails'), e['version']), e['playerOutput']), call(e['getSectionFooter'])))
    return e['output']
    return U


def callback_220(parent, this, args):
    # Upstream checkup: 5085
    e = Env(parent)
    e.declare(['checkVal', 'fields', 'hasIt', 'txt'])
    e.local['arguments'] = Array(args)
    e.local['k'] = (args[0] if len(args) > 0 and args[0] is not U else U)
    e.set('fields', call(get(get(get(e['meta'], 'bookpowers'), e['k']), 'split'), ' '))
    e.set('hasIt', False)
    e.set('checkVal', (get(e['fields'], 3) if truth(binary('>', get(e['fields'], 'length'), 3)) else True))
    if truth(binary('===', get(e['fields'], 1), 'Host')):
        e.set('hasIt', (binary('>=', get(get(get(get(e['saveInfo'], 'data'), get(e['saveInfo'], 'farmerId')), get(get(e['meta'], 'query'), get(e['fields'], 0))), get(e['fields'], 2)), e['checkVal']) if truth(_logic221 := call(get(get(get(get(e['saveInfo'], 'data'), get(e['saveInfo'], 'farmerId')), get(get(e['meta'], 'query'), get(e['fields'], 0))), 'hasOwnProperty'), get(e['fields'], 2))) else _logic221))
    if truth(unary('!', e['hasIt'])):
        e.set('hasIt', (binary('>=', get(get(get(get(e['saveInfo'], 'data'), e['umid']), get(get(e['meta'], 'query'), get(e['fields'], 0))), get(e['fields'], 2)), e['checkVal']) if truth(_logic222 := call(get(get(get(get(e['saveInfo'], 'data'), e['umid']), get(get(e['meta'], 'query'), get(e['fields'], 0))), 'hasOwnProperty'), get(e['fields'], 2))) else _logic222))
    if truth(e['hasIt']):
        update_env(e, 'have_book', 1, False)
    else:
        e.set('txt', e['k'])
        if truth(call(get(get(e['meta'], 'translate'), 'hasOwnProperty'), e['k'])):
            e.set('txt', get(get(e['meta'], 'translate'), e['k']))
        else:
            if truth(call(get(get(e['saveInfo'], 'objects'), 'hasOwnProperty'), e['k'])):
                e.set('txt', get(get(e['saveInfo'], 'objects'), e['k']))
        call(get(e['need'], 'push'), binary('+', binary('+', '<li><span class="booktitle">', e['txt']), '</span></li>'))
    return U


def callback_223(parent, this, args):
    # Upstream checkup: 5114
    e = Env(parent)
    e.declare(['checkVal', 'fields', 'hasIt', 'txt'])
    e.local['arguments'] = Array(args)
    e.local['k'] = (args[0] if len(args) > 0 and args[0] is not U else U)
    e.set('fields', call(get(get(get(e['meta'], 'otherpowers'), e['k']), 'split'), ' '))
    e.set('hasIt', False)
    e.set('checkVal', (get(e['fields'], 3) if truth(binary('>', get(e['fields'], 'length'), 3)) else True))
    if truth(binary('===', get(e['fields'], 1), 'Host')):
        e.set('hasIt', (binary('===', get(get(get(get(e['saveInfo'], 'data'), get(e['saveInfo'], 'farmerId')), get(get(e['meta'], 'query'), get(e['fields'], 0))), get(e['fields'], 2)), e['checkVal']) if truth(_logic224 := call(get(get(get(get(e['saveInfo'], 'data'), get(e['saveInfo'], 'farmerId')), get(get(e['meta'], 'query'), get(e['fields'], 0))), 'hasOwnProperty'), get(e['fields'], 2))) else _logic224))
    if truth(unary('!', e['hasIt'])):
        e.set('hasIt', (binary('===', get(get(get(get(e['saveInfo'], 'data'), e['umid']), get(get(e['meta'], 'query'), get(e['fields'], 0))), get(e['fields'], 2)), e['checkVal']) if truth(_logic225 := call(get(get(get(get(e['saveInfo'], 'data'), e['umid']), get(get(e['meta'], 'query'), get(e['fields'], 0))), 'hasOwnProperty'), get(e['fields'], 2))) else _logic225))
    if truth(e['hasIt']):
        update_env(e, 'have_other', 1, False)
    else:
        e.set('txt', e['k'])
        if truth(call(get(get(e['meta'], 'translate'), 'hasOwnProperty'), e['k'])):
            e.set('txt', get(get(e['meta'], 'translate'), e['k']))
        else:
            if truth(call(get(get(e['saveInfo'], 'objects'), 'hasOwnProperty'), e['k'])):
                e.set('txt', get(get(e['saveInfo'], 'objects'), e['k']))
        call(get(e['need'], 'push'), binary('+', binary('+', '<li>', e['txt']), '</li>'))
    return U


def parsePlayerPowers_219(parent, this, args):
    # Upstream checkup: 5074
    e = Env(parent)
    e.declare(['book_count', 'have_book', 'have_other', 'id', 'need', 'other_count', 'output', 'power_count', 'umid'])
    e.local['arguments'] = Array(args)
    e.local['player'] = (args[0] if len(args) > 0 and args[0] is not U else U)
    e.local['saveInfo'] = (args[1] if len(args) > 1 and args[1] is not U else U)
    e.local['meta'] = (args[2] if len(args) > 2 and args[2] is not U else U)
    e.set('output', '')
    e.set('have_book', 0)
    e.set('have_other', 0)
    e.set('umid', call(get(call(get(call(e['$'], e['player']), 'children'), 'UniqueMultiplayerID'), 'text')))
    e.set('need', Array([]))
    e.set('book_count', get(call(get(e['Object'], 'keys'), get(e['meta'], 'bookpowers')), 'length'))
    e.set('other_count', get(call(get(e['Object'], 'keys'), get(e['meta'], 'otherpowers')), 'length'))
    e.set('power_count', binary('+', e['book_count'], e['other_count']))
    call(get(call(get(e['Object'], 'keys'), get(e['meta'], 'bookpowers')), 'forEach'), Fn(callback_220, e))
    call(get(call(get(e['Object'], 'keys'), get(e['meta'], 'otherpowers')), 'forEach'), Fn(callback_223, e))
    e.set('output', binary('+', e['output'], binary('+', binary('+', binary('+', binary('+', '<div class="', get(e['meta'], 'anchor')), '_summary '), get(e['meta'], 'sum_class')), '">')))
    e.set('output', binary('+', e['output'], binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', '<span class="result">', get(get(e['saveInfo'], 'players'), e['umid'])), ' has read '), e['have_book']), ' of '), e['book_count']), ' books.</span><br />\n')))
    e.set('output', binary('+', e['output'], '<ul class="ach_list"><li>'))
    e.set('output', binary('+', e['output'], (call(e['getAchieveString'], 'Well Read', 'Read all books', 1) if truth(binary('>=', e['have_book'], e['book_count'])) else binary('+', binary('+', call(e['getAchieveString'], 'Well-read', 'Read all books', 0), binary('-', e['book_count'], e['have_book'])), ' more'))))
    e.set('output', binary('+', e['output'], '</li></ul></div>'))
    e.set('output', binary('+', e['output'], binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', '<span class="result">', get(get(e['saveInfo'], 'players'), e['umid'])), ' has received '), e['have_other']), ' of '), e['other_count']), ' special items &amp; powers.</span><br />\n')))
    e.set('output', binary('+', e['output'], '<ul class="ach_list"><li>'))
    e.set('output', binary('+', e['output'], (call(e['getMilestoneString'], 'Acquire all special items &amp; powers', 1) if truth(binary('>=', e['have_other'], e['other_count'])) else binary('+', binary('+', call(e['getMilestoneString'], 'Acquire all special items &amp; powers', 0), binary('-', e['other_count'], e['have_other'])), ' more'))))
    e.set('output', binary('+', e['output'], '</li></ul></div>'))
    if truth(binary('>', get(e['need'], 'length'), 0)):
        put(e['meta'], 'hasDetails', True)
        e.set('output', binary('+', e['output'], binary('+', binary('+', binary('+', binary('+', '<div class="', get(e['meta'], 'anchor')), '_details '), get(e['meta'], 'det_class')), '">')))
        e.set('output', binary('+', e['output'], '<span class="need">Left:'))
        if truth(binary('<', e['have_book'], e['book_count'])):
            e.set('output', binary('+', e['output'], ' (Books listed first)'))
        e.set('output', binary('+', e['output'], binary('+', binary('+', '<ol>', call(get(call(get(e['need'], 'sort')), 'join'), '')), '</ol></span></div>')))
    return Array([e['output']])
    return U


def callback_227(parent, this, args):
    # Upstream checkup: 5184
    e = Env(parent)
    e.declare([])
    e.local['arguments'] = Array(args)
    call(get(e['table'], 'push'), binary('+', binary('+', binary('+', binary('+', '<li>', call(e['addCommas'], call(get(call(get(call(e['$'], this), 'find'), 'score > *'), 'text')))), ' &ndash; '), call(get(call(get(call(e['$'], this), 'find'), 'name > *'), 'text'))), '</li>'))
    return U


def parseArcadeGames_226(parent, this, args):
    # Upstream checkup: 5164
    e = Env(parent)
    e.declare(['anchor', 'det_class', 'meta', 'output', 'playerOutput', 'sum_class', 'table', 'title', 'version'])
    e.local['arguments'] = Array(args)
    e.local['xmlDoc'] = (args[0] if len(args) > 0 and args[0] is not U else U)
    e.local['saveInfo'] = (args[1] if len(args) > 1 and args[1] is not U else U)
    e.set('title', 'Arcade Games')
    e.set('anchor', call(e['makeAnchor'], e['title']))
    e.set('version', '1.5')
    e.set('sum_class', call(e['getSummaryClass'], e['saveInfo'], e['version']))
    e.set('det_class', call(e['getDetailsClass'], e['saveInfo'], e['version']))
    e.set('output', '')
    e.set('playerOutput', '')
    e.set('table', Array([]))
    e.set('meta', Obj({'hasDetails': False, 'anchor': e['anchor'], 'sum_class': e['sum_class'], 'det_class': e['det_class']}))
    if truth(binary('<', call(e['compareSemVer'], get(e['saveInfo'], 'version'), e['version']), 0)):
        return ''
    put(e['table'], 0, call(e['parsePlayerArcade'], call(get(call(e['$'], e['xmlDoc']), 'find'), 'SaveGame > player'), e['saveInfo'], e['meta']))
    call(e['parseFarmhands'], e['xmlDoc'], e['saveInfo'], e['table'], e['parsePlayerArcade'], e['meta'])
    e.set('playerOutput', binary('+', e['playerOutput'], call(e['printTranspose'], e['table'])))
    e.set('table', Array([]))
    call(get(call(get(call(e['$'], e['xmlDoc']), 'find'), 'junimoKartLeaderboards > entries > NetLeaderboardsEntry'), 'each'), Fn(callback_227, e))
    put(e['meta'], 'hasDetails', binary('>', get(e['table'], 'length'), 0))
    e.set('output', binary('+', call(e['getSectionHeader'], e['saveInfo'], e['title'], e['anchor'], get(e['meta'], 'hasDetails'), e['version']), e['playerOutput']))
    if truth(binary('>', get(e['table'], 'length'), 0)):
        e.set('output', binary('+', e['output'], binary('+', binary('+', binary('+', binary('+', '<div class="', get(e['meta'], 'anchor')), '_details '), get(e['meta'], 'det_class')), '">')))
        e.set('output', binary('+', e['output'], '<span class="result">Junimo Kart (Endless Mode) Leaderboard:</span><ol class="outer">'))
        e.set('output', binary('+', e['output'], call(get(e['table'], 'join'), '')))
        e.set('output', binary('+', e['output'], '</ol></div>'))
    e.set('output', binary('+', e['output'], call(e['getSectionFooter'])))
    return e['output']
    return U


def parsePlayerArcade_228(parent, this, args):
    # Upstream checkup: 5200
    e = Env(parent)
    e.declare(['hasBeatenJK', 'hasBeatenPK', 'level', 'need', 'output', 'pkProgress', 'pkSave', 'sublevel', 'umid'])
    e.local['arguments'] = Array(args)
    e.local['player'] = (args[0] if len(args) > 0 and args[0] is not U else U)
    e.local['saveInfo'] = (args[1] if len(args) > 1 and args[1] is not U else U)
    e.local['meta'] = (args[2] if len(args) > 2 and args[2] is not U else U)
    e.set('output', '')
    e.set('umid', call(get(call(get(call(e['$'], e['player']), 'children'), 'UniqueMultiplayerID'), 'text')))
    e.set('hasBeatenPK', call(get(get(get(get(e['saveInfo'], 'data'), e['umid']), 'mailReceived'), 'hasOwnProperty'), 'Beat_PK'))
    e.set('hasBeatenJK', call(get(get(get(get(e['saveInfo'], 'data'), e['umid']), 'mailReceived'), 'hasOwnProperty'), 'JunimoKart'))
    e.set('need', Array([]))
    e.set('output', binary('+', e['output'], binary('+', binary('+', binary('+', binary('+', '<div class="', get(e['meta'], 'anchor')), '_summary '), get(e['meta'], 'sum_class')), '">')))
    e.set('output', binary('+', e['output'], binary('+', binary('+', binary('+', binary('+', '<span class="result">', get(get(e['saveInfo'], 'players'), e['umid'])), ' has'), ('' if truth(e['hasBeatenPK']) else ' not')), ' beaten Journey of the Prairie King.</span><br/>')))
    e.set('pkProgress', 0)
    e.set('pkSave', call(get(call(e['$'], e['player']), 'children'), 'JOTPKProgress'))
    if truth(binary('>', get(e['pkSave'], 'length'), 0)):
        e.set('level', binary('+', 1, call(e['Number'], call(get(call(get(call(e['$'], e['pkSave']), 'find'), 'whichRound > int'), 'text')))))
        e.set('sublevel', binary('+', 1, call(e['Number'], call(get(call(get(call(e['$'], e['pkSave']), 'find'), 'whichWave > int'), 'text')))))
        e.set('output', binary('+', e['output'], binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', '<span class="result">', get(get(e['saveInfo'], 'players'), e['umid'])), ' has a JotPK save at stage '), e['level']), '-'), e['sublevel']), ' ('), ('not ' if truth(binary('===', call(get(call(get(call(e['$'], e['pkSave']), 'find'), 'died > boolean'), 'text')), 'true')) else '')), 'deathless)</span><br/>')))
        e.set('pkProgress', (8 if truth(binary('==', e['level'], 3)) else binary('+', (4 if truth(binary('==', e['level'], 2)) else unary('-', 1)), e['sublevel'])))
    else:
        e.set('output', binary('+', e['output'], binary('+', binary('+', '<span class="result">', get(get(e['saveInfo'], 'players'), e['umid'])), ' does not have a saved JotPK game.')))
    e.set('output', binary('+', e['output'], '<ul class="ach_list"><li>'))
    e.set('output', binary('+', e['output'], (call(e['getAchieveString'], 'Prairie King', "Beat 'Journey of the Prairie King'", 1) if truth(e['hasBeatenPK']) else binary('+', binary('+', binary('+', call(e['getAchieveString'], 'Prairie King', "Beat 'Journey of the Prairie King'", 0), ' to clear '), binary('-', 13, e['pkProgress'])), ' more level(s)'))))
    e.set('output', binary('+', e['output'], '</li></ul>'))
    e.set('output', binary('+', e['output'], binary('+', binary('+', binary('+', binary('+', '<span class="result">', get(get(e['saveInfo'], 'players'), e['umid'])), ' has'), ('' if truth(e['hasBeatenJK']) else ' not')), ' beaten Junimo Kart (Progress Mode).</span><br/>')))
    e.set('output', binary('+', e['output'], '<ul class="ach_list"><li>'))
    e.set('output', binary('+', e['output'], (call(e['getMilestoneString'], "Beat 'Junimo Kart'", 1) if truth(e['hasBeatenJK']) else binary('+', call(e['getMilestoneString'], "Beat 'Junimo Kart'", 0), ' to complete Progress Mode'))))
    e.set('output', binary('+', e['output'], '</li></ul>'))
    e.set('output', binary('+', e['output'], '</div>'))
    return Array([e['output']])
    return U


def callback_230(parent, this, args):
    # Upstream checkup: 5252
    e = Env(parent)
    e.declare(['thisPetLove', 'type'])
    e.local['arguments'] = Array(args)
    if truth((_logic231 if truth(_logic231 := (_logic232 if truth(_logic232 := binary('===', call(get(call(e['$'], this), 'attr'), binary('+', get(e['saveInfo'], 'ns_prefix'), ':type')), 'Pet')) else binary('===', call(get(call(e['$'], this), 'attr'), binary('+', get(e['saveInfo'], 'ns_prefix'), ':type')), 'Cat'))) else binary('===', call(get(call(e['$'], this), 'attr'), binary('+', get(e['saveInfo'], 'ns_prefix'), ':type')), 'Dog'))):
        e.set('type', call(get(call(get(call(e['$'], this), 'find'), 'petType'), 'text')))
        e.set('thisPetLove', call(e['Number'], call(get(call(get(call(e['$'], this), 'find'), 'friendshipTowardFarmer'), 'text'))))
        call(get(e['list'], 'push'), binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', '<li>', e['type']), ' named '), call(get(call(get(call(get(call(e['$'], this), 'find'), 'name'), 'first')), 'text'))), ' ('), e['thisPetLove']), ' friendship points)</li>'))
    return U


def callback_239(parent, this, args):
    # Upstream checkup: 5272
    e = Env(parent)
    e.declare(['cracker', 'extra', 'type'])
    e.local['arguments'] = Array(args)
    e.set('cracker', binary('===', call(get(call(get(call(e['$'], this), 'find'), 'hasEatenAnimalCracker'), 'text')), 'true'))
    e.set('type', call(get(call(get(call(e['$'], this), 'find'), 'type'), 'text')))
    if truth(binary('===', e['type'], 'Pig')):
        e.set('extra', ' [<span class="ms_imp">cannot eat cracker</span>]')
    else:
        e.set('extra', (' [<span class="ms_yes">has eaten cracker</span>]' if truth(e['cracker']) else ' [<span class="ms_no">has not eaten cracker</span>]'))
    call(get(e['list'], 'push'), binary('+', binary('+', binary('+', binary('+', binary('+', '<li>', e['type']), ' named '), call(get(call(get(call(e['$'], this), 'find'), 'name'), 'text'))), e['extra']), '</li>'))
    return U


def callback_233(parent, this, args):
    # Upstream checkup: 5266
    e = Env(parent)
    e.declare(['btype', 'cur', 'list', 'max'])
    e.local['arguments'] = Array(args)
    e.set('btype', call(get(call(get(call(e['$'], this), 'find'), 'buildingType'), 'text')))
    e.set('cur', call(get(call(get(call(e['$'], this), 'find'), 'currentOccupants'), 'text')))
    e.set('max', call(get(call(get(call(e['$'], this), 'find'), 'maxOccupants'), 'text')))
    if truth((_logic234 if truth(_logic234 := (_logic235 if truth(_logic235 := (_logic236 if truth(_logic236 := (_logic237 if truth(_logic237 := (_logic238 if truth(_logic238 := binary('===', e['btype'], 'Coop')) else binary('===', e['btype'], 'Big Coop'))) else binary('===', e['btype'], 'Deluxe Coop'))) else binary('===', e['btype'], 'Barn'))) else binary('===', e['btype'], 'Big Barn'))) else binary('===', e['btype'], 'Deluxe Barn'))):
        e.set('list', Array([]))
        call(get(call(get(call(e['$'], this), 'find'), 'indoors > Animals > SerializableDictionaryOfInt64FarmAnimal FarmAnimal'), 'each'), Fn(callback_239, e))
        e.set('output', binary('+', e['output'], binary('+', binary('+', binary('+', binary('+', '<div class="', get(e['meta'], 'anchor')), '_summary '), get(e['meta'], 'sum_class')), '">')))
        e.set('output', binary('+', e['output'], binary('+', binary('+', binary('+', binary('+', binary('+', binary('+', '<span class="result">', e['btype']), ' ('), e['cur']), '/'), e['max']), ')</span></div>')))
        e.set('output', binary('+', e['output'], binary('+', binary('+', binary('+', binary('+', '<div class="', get(e['meta'], 'anchor')), '_details '), get(e['meta'], 'det_class')), '"><ol class="outer">')))
        e.set('output', binary('+', e['output'], binary('+', call(get(call(get(e['list'], 'sort')), 'join'), ''), '</ol></div>')))
    return U


def parseAnimals_229(parent, this, args):
    # Upstream checkup: 5235
    e = Env(parent)
    e.declare(['anchor', 'det_class', 'list', 'meta', 'output', 'playerOutput', 'sum_class', 'title', 'version'])
    e.local['arguments'] = Array(args)
    e.local['xmlDoc'] = (args[0] if len(args) > 0 and args[0] is not U else U)
    e.local['saveInfo'] = (args[1] if len(args) > 1 and args[1] is not U else U)
    e.set('title', 'Animal Summary')
    e.set('anchor', call(e['makeAnchor'], e['title']))
    e.set('version', '1.6')
    e.set('sum_class', call(e['getSummaryClass'], e['saveInfo'], e['version']))
    e.set('det_class', call(e['getDetailsClass'], e['saveInfo'], e['version']))
    e.set('output', '')
    e.set('playerOutput', '')
    e.set('meta', Obj({'hasDetails': False, 'anchor': e['anchor'], 'sum_class': e['sum_class'], 'det_class': e['det_class']}))
    if truth(binary('<', call(e['compareSemVer'], get(e['saveInfo'], 'version'), e['version']), 0)):
        return ''
    put(e['meta'], 'hasDetails', True)
    e.set('list', Array([]))
    call(get(call(get(call(e['$'], e['xmlDoc']), 'find'), 'locations > GameLocation > Characters > NPC'), 'each'), Fn(callback_230, e))
    e.set('output', binary('+', e['output'], binary('+', binary('+', binary('+', binary('+', '<div class="', get(e['meta'], 'anchor')), '_summary '), get(e['meta'], 'sum_class')), '">')))
    e.set('output', binary('+', e['output'], binary('+', binary('+', '<span class="result">Farm Pets (', get(e['list'], 'length')), ')</span></div>')))
    e.set('output', binary('+', e['output'], binary('+', binary('+', binary('+', binary('+', '<div class="', get(e['meta'], 'anchor')), '_details '), get(e['meta'], 'det_class')), '">')))
    e.set('output', binary('+', e['output'], binary('+', binary('+', '<ol class="outer">', call(get(call(get(e['list'], 'sort')), 'join'), '')), '</ol>')))
    e.set('output', binary('+', e['output'], '</div>'))
    call(get(call(get(call(e['$'], e['xmlDoc']), 'find'), binary('+', binary('+', '[', get(e['saveInfo'], 'ns_prefix')), "\\:type='Farm'] Building")), 'each'), Fn(callback_233, e))
    e.set('output', binary('+', binary('+', call(e['getSectionHeader'], e['saveInfo'], e['title'], e['anchor'], get(e['meta'], 'hasDetails'), e['version']), e['output']), call(e['getSectionFooter'])))
    return e['output']
    return U


def parseRaccoons_240(parent, this, args):
    # Upstream checkup: 5293
    e = Env(parent)
    e.declare(['anchor', 'checkBundles', 'daysSinceFed', 'det_class', 'id', 'intro', 'lastFed', 'meta', 'output', 'playerOutput', 'sum_class', 'timesFed', 'title', 'version'])
    e.local['arguments'] = Array(args)
    e.local['xmlDoc'] = (args[0] if len(args) > 0 and args[0] is not U else U)
    e.local['saveInfo'] = (args[1] if len(args) > 1 and args[1] is not U else U)
    e.set('title', 'Forest Neighbors')
    e.set('anchor', call(e['makeAnchor'], e['title']))
    e.set('version', '1.6')
    e.set('sum_class', call(e['getSummaryClass'], e['saveInfo'], e['version']))
    e.set('det_class', call(e['getDetailsClass'], e['saveInfo'], e['version']))
    e.set('output', '')
    e.set('playerOutput', '')
    e.set('meta', Obj({'hasDetails': False, 'anchor': e['anchor'], 'sum_class': e['sum_class'], 'det_class': e['det_class']}))
    e.set('timesFed', call(e['Number'], call(get(call(get(call(e['$'], e['xmlDoc']), 'find'), 'SaveGame > timesFedRaccoons'), 'text'))))
    e.set('lastFed', call(e['Number'], call(get(call(get(call(e['$'], e['xmlDoc']), 'find'), 'SaveGame > daysPlayedWhenLastRaccoonBundleWasFinished'), 'text'))))
    e.set('daysSinceFed', binary('-', get(get(get(get(e['saveInfo'], 'data'), get(e['saveInfo'], 'farmerId')), 'stats'), 'daysPlayed'), e['lastFed']))
    e.set('checkBundles', False)
    if truth(binary('<', call(e['compareSemVer'], get(e['saveInfo'], 'version'), e['version']), 0)):
        return ''
    if truth(call(get(get(get(get(e['saveInfo'], 'data'), get(e['saveInfo'], 'farmerId')), 'mailReceived'), 'hasOwnProperty'), 'raccoonMovedIn')):
        e.set('intro', 'Mr. Raccoon has moved into the refurbished stump in the forest.')
        e.set('checkBundles', True)
    else:
        if truth(call(get(get(get(get(e['saveInfo'], 'data'), get(e['saveInfo'], 'farmerId')), 'mailReceived'), 'hasOwnProperty'), 'raccoonTreeFallen')):
            e.set('intro', 'The big tree in the forest has fallen and repairs may be needed.')
        else:
            if truth((_logic241 if truth(_logic241 := call(get(get(get(get(e['saveInfo'], 'data'), get(e['saveInfo'], 'farmerId')), 'mailReceived'), 'hasOwnProperty'), 'ccPantry')) else call(get(get(get(get(e['saveInfo'], 'data'), get(e['saveInfo'], 'farmerId')), 'mailReceived'), 'hasOwnProperty'), 'jojaPantry'))):
                e.set('intro', 'The Greenhouse has been repaired. Where did that raccoon go?')
            else:
                e.set('intro', 'The Greenhouse has not yet been repaired.')
    e.set('output', binary('+', binary('+', binary('+', binary('+', '<div class="', get(e['meta'], 'anchor')), '_summary '), get(e['meta'], 'sum_class')), '">'))
    e.set('output', binary('+', e['output'], binary('+', binary('+', '<span class="result">', e['intro']), '</span><br />\n')))
    e.set('output', binary('+', e['output'], binary('+', binary('+', '<span class="result">The neighbors have been helped ', e['timesFed']), ' times')))
    if truth(binary('>', e['lastFed'], 0)):
        e.set('output', binary('+', e['output'], binary('+', binary('+', ' (most recently ', e['daysSinceFed']), ' days ago)')))
    e.set('output', binary('+', e['output'], '.</span><br />\n'))
    e.set('output', binary('+', e['output'], '<ul class="ach_list"><li>'))
    if truth((_logic242 if truth(_logic242 := binary('>', e['timesFed'], 9)) else (binary('>', e['daysSinceFed'], 7) if truth(_logic243 := binary('==', e['timesFed'], 9)) else _logic243))):
        e.set('output', binary('+', e['output'], call(e['getAchieveString'], 'Good Neighbors', 'help your forest neighbors grow their family', 1)))
    else:
        if truth((binary('<=', e['daysSinceFed'], 7) if truth(_logic244 := binary('==', e['timesFed'], 9)) else _logic244)):
            e.set('output', binary('+', e['output'], binary('+', call(e['getAchieveString'], 'Good Neighbors', 'help your forest neighbors grow their family', 0), 'to wait a few more days')))
        else:
            e.set('output', binary('+', e['output'], binary('+', binary('+', binary('+', call(e['getAchieveString'], 'Good Neighbors', 'help your forest neighbors grow their family', 0), 'to help '), binary('-', 9, e['timesFed'])), ' more times')))
    e.set('output', binary('+', binary('+', call(e['getSectionHeader'], e['saveInfo'], e['title'], e['anchor'], get(e['meta'], 'hasDetails'), e['version']), e['output']), call(e['getSectionFooter'])))
    return e['output']
    return U

def create(environment):
    e = Env(environment)
    e.local["save"] = Obj()
    e.local['addCommas'] = Fn(addCommas_1, e)
    e.local['capitalize'] = Fn(capitalize_2, e)
    e.local['compareSemVer'] = Fn(compareSemVer_4, e)
    e.local['getAchieveString'] = Fn(getAchieveString_7, e)
    e.local['getAchieveImpossibleString'] = Fn(getAchieveImpossibleString_8, e)
    e.local['getMilestoneString'] = Fn(getMilestoneString_9, e)
    e.local['getPointString'] = Fn(getPointString_10, e)
    e.local['getPointImpossibleString'] = Fn(getPointImpossibleString_11, e)
    e.local['getPerfectionPctString'] = Fn(getPerfectionPctString_12, e)
    e.local['getPerfectionNumString'] = Fn(getPerfectionNumString_14, e)
    e.local['getPerfectionPctNumString'] = Fn(getPerfectionPctNumString_15, e)
    e.local['getPerfectionBoolString'] = Fn(getPerfectionBoolString_17, e)
    e.local['wikify'] = Fn(wikify_18, e)
    e.local['wikimap'] = Fn(wikimap_19, e)
    e.local['printTranspose'] = Fn(printTranspose_20, e)
    e.local['isValidFarmhand'] = Fn(isValidFarmhand_21, e)
    e.local['getSummaryClass'] = Fn(getSummaryClass_23, e)
    e.local['getDetailsClass'] = Fn(getDetailsClass_25, e)
    e.local['getPTLink'] = Fn(getPTLink_27, e)
    e.local['getSectionHeader'] = Fn(getSectionHeader_28, e)
    e.local['getSectionFooter'] = Fn(getSectionFooter_31, e)
    e.local['collapsibleWrap'] = Fn(collapsibleWrap_32, e)
    e.local['makeAnchor'] = Fn(makeAnchor_33, e)
    e.local['parseSummary'] = Fn(parseSummary_34, e)
    e.local['parseFarmhands'] = Fn(parseFarmhands_40, e)
    e.local['populateData'] = Fn(populateData_42, e)
    e.local['parseMoney'] = Fn(parseMoney_48, e)
    e.local['parseSocial'] = Fn(parseSocial_51, e)
    e.local['parsePlayerSocial'] = Fn(parsePlayerSocial_56, e)
    e.local['parseFamily'] = Fn(parseFamily_88, e)
    e.local['parsePlayerFamily'] = Fn(parsePlayerFamily_89, e)
    e.local['parseCooking'] = Fn(parseCooking_96, e)
    e.local['parsePlayerCooking'] = Fn(parsePlayerCooking_98, e)
    e.local['parseCrafting'] = Fn(parseCrafting_102, e)
    e.local['parsePlayerCrafting'] = Fn(parsePlayerCrafting_103, e)
    e.local['parseFishing'] = Fn(parseFishing_106, e)
    e.local['parsePlayerFishing'] = Fn(parsePlayerFishing_107, e)
    e.local['parseBasicShipping'] = Fn(parseBasicShipping_112, e)
    e.local['parsePlayerBasicShipping'] = Fn(parsePlayerBasicShipping_113, e)
    e.local['parseCropShipping'] = Fn(parseCropShipping_117, e)
    e.local['parsePlayerCropShipping'] = Fn(parsePlayerCropShipping_118, e)
    e.local['parseSkills'] = Fn(parseSkills_121, e)
    e.local['parsePlayerSkills'] = Fn(parsePlayerSkills_122, e)
    e.local['parseSkillMastery'] = Fn(parseSkillMastery_124, e)
    e.local['parsePlayerSkillMastery'] = Fn(parsePlayerSkillMastery_125, e)
    e.local['parseMuseum'] = Fn(parseMuseum_127, e)
    e.local['parsePlayerMuseum'] = Fn(parsePlayerMuseum_130, e)
    e.local['parseMonsters'] = Fn(parseMonsters_138, e)
    e.local['parsePlayerMonsters'] = Fn(parsePlayerMonsters_139, e)
    e.local['parseQuests'] = Fn(parseQuests_143, e)
    e.local['parsePlayerQuests'] = Fn(parsePlayerQuests_144, e)
    e.local['parseStardrops'] = Fn(parseStardrops_145, e)
    e.local['parsePlayerStardrops'] = Fn(parsePlayerStardrops_146, e)
    e.local['parseGrandpa'] = Fn(parseGrandpa_153, e)
    e.local['parseBundleData'] = Fn(parseBundleData_165, e)
    e.local['parseBundles'] = Fn(parseBundles_167, e)
    e.local['parseSecretNotes'] = Fn(parseSecretNotes_180, e)
    e.local['parsePlayerSecretNotes'] = Fn(parsePlayerSecretNotes_184, e)
    e.local['parseJournalScraps'] = Fn(parseJournalScraps_188, e)
    e.local['parsePlayerJournalScraps'] = Fn(parsePlayerJournalScraps_189, e)
    e.local['parseSpecialOrders'] = Fn(parseSpecialOrders_195, e)
    e.local['parseWalnuts'] = Fn(parseWalnuts_198, e)
    e.local['parseIslandUpgrades'] = Fn(parseIslandUpgrades_206, e)
    e.local['parsePerfectionTracker'] = Fn(parsePerfectionTracker_210, e)
    e.local['parsePlayerPerfection'] = Fn(parsePlayerPerfection_217, e)
    e.local['parsePowers'] = Fn(parsePowers_218, e)
    e.local['parsePlayerPowers'] = Fn(parsePlayerPowers_219, e)
    e.local['parseArcadeGames'] = Fn(parseArcadeGames_226, e)
    e.local['parsePlayerArcade'] = Fn(parsePlayerArcade_228, e)
    e.local['parseAnimals'] = Fn(parseAnimals_229, e)
    e.local['parseRaccoons'] = Fn(parseRaccoons_240, e)
    return e

"""Purpose-built forms. Each form validates in the browser, then opens a
pre-filled email to the right inbox (data-to) with a clear subject line."""
from html import escape

KNOB = '<span class="knob"><i class="ph-light ph-arrow-up-right"></i></span>'


def _esc(s):
    return escape(s, quote=True)


def field(fid, kind, name, label, req=False, opts=None, full=False, auto='', ph='', err='', inputmode=''):
    """kind: text, email, tel, date, time, number, select, textarea, checks, check."""
    i = f'{fid}-{name}'
    cls = 'field' + (' full' if full or kind in ('textarea', 'checks', 'check') else '')
    star = ' <span class="opt">required</span>' if req else ''
    r = ' required' if req else ''
    a = f' autocomplete="{auto}"' if auto else ''
    p = f' placeholder="{_esc(ph)}"' if ph else ''
    im = f' inputmode="{inputmode}"' if inputmode else ''
    msg = err or ('Please enter a valid email address.' if kind == 'email' else 'Please complete this field.')
    e = f'<span class="err">{msg}</span>' if req else ''
    lab = f'<label for="{i}" data-l="{_esc(label)}">{label}{star}</label>'
    if kind == 'select':
        o = ''.join(f'<option>{_esc(x)}</option>' for x in opts)
        first = '<option value="">Select one</option>' if req else ''
        return f'<div class="{cls}">{lab}<select id="{i}" name="{name}"{r}>{first}{o}</select>{e}</div>'
    if kind == 'textarea':
        return f'<div class="{cls}">{lab}<textarea id="{i}" name="{name}"{r}{p}></textarea>{e}</div>'
    if kind == 'checks':
        boxes = ''.join(f'<label><input type="checkbox" name="{name}" value="{_esc(x)}">{_esc(x)}</label>' for x in opts)
        return f'<div class="{cls}"><span class="flabel" id="{i}">{label}</span><div class="checks" role="group" aria-labelledby="{i}" data-group="{_esc(label)}">{boxes}</div></div>'
    if kind == 'check':
        return f'<div class="{cls}"><label class="consent"><input type="checkbox" id="{i}" name="{name}" data-l="{_esc(opts or label)}"{r}><span>{label}</span></label>{e}</div>'
    return f'<div class="{cls}">{lab}<input id="{i}" name="{name}" type="{kind}"{a}{p}{im}{r}>{e}</div>'


def form(fid, to, subject, fields, button, note):
    return (f'<form class="bezel reveal cp-form" novalidate id="{fid}" data-to="{to}" data-subject="{_esc(subject)}"><div class="core">'
            f'<div class="fgrid">{"".join(fields)}</div>'
            f'<button class="btn btn-navy" type="submit">{button} {KNOB}</button>'
            f'<p class="fnote" role="status" aria-live="polite">{note}</p>'
            f'<noscript><p class="fnote">This form needs JavaScript. Email <a href="mailto:{to}?subject={_esc(subject)}">{to}</a> instead.</p></noscript>'
            '</div></form>')


def form_section(h2, intro, contacts, form_html, sid='form'):
    lis = ''.join(f'<li><i class="ph-light {ic}"></i><div><strong>{a}</strong><span>{b}</span></div></li>' for ic, a, b in contacts)
    return (f'<section class="block proposal" id="{sid}"><div class="wrap prop-grid">'
            f'<div class="reveal"><h2>{h2}</h2><p class="intro">{intro}</p><ul class="clist">{lis}</ul></div>'
            f'{form_html}</div></section>')

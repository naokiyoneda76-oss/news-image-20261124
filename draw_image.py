#!/usr/bin/env python3
"""Render the 24 November 2026 world-news competition image."""
import os
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

S = 2
W = H = 1024
CREAM = '#F4EFE3'
NAVY = '#152A44'
GOLD = '#D9A441'
INK = '#1B2A3B'
BODY = '#33475B'
WHITE = '#FFFFFF'
REG = '/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf'
BOLD = '/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf'
im = Image.new('RGB', (W*S, H*S), CREAM)
d = ImageDraw.Draw(im)

def box(coords): return tuple(round(v*S) for v in coords)
def font(size, bold=False): return ImageFont.truetype(BOLD if bold else REG, round(size*S))
def rect(coords, fill, outline=None, width=1, radius=0):
    b=box(coords)
    if radius: d.rounded_rectangle(b, radius=radius*S, fill=fill, outline=outline, width=width*S)
    else: d.rectangle(b, fill=fill, outline=outline, width=width*S)
def line(points, fill, width=1): d.line([box(p) for p in points], fill=fill, width=max(1,width*S), joint='curve')
def ellipse(coords, fill=None, outline=None, width=1): d.ellipse(box(coords), fill=fill, outline=outline, width=width*S)
def txt(pos, text, size, fill, bold=False, anchor=None):
    d.text(box(pos), text, font=font(size,bold), fill=fill, anchor=anchor)
def width(text, size, bold=False): return d.textbbox((0,0), text, font=font(size,bold))[2]/S
def checked_lines(lines, size, bold, lane, label):
    for n, line_text in enumerate(lines):
        assert width(line_text,size,bold) <= lane, f'{label} line {n+1} too wide: {width(line_text,size,bold):.1f}>{lane}'

# Masthead
rect((0,0,1024,136), NAVY)
txt((48,8),'THE DAY IN ONE PICTURE',24,GOLD,True)
txt((46,30),'24 NOVEMBER 2026',76,WHITE,True)
txt((48,106),'Tuesday · World news, summed up in one image',22,'#E8EDF4')
rect((0,150,1024,155),'#C9982F')

# Lead story
rect((0,155,1024,413),'#8E2B27')
cw = width('TECH · NVIDIA', 23, True) + 24
rect((48,171,48+cw,201),'#8E2B27',outline='#D98E4A',width=1,radius=8)
txt((60,173),'TECH · NVIDIA',23,WHITE,True)
hero_head=['Jensen Huang Returns','to Lead Nvidia Again']
checked_lines(hero_head,46,True,620,'hero headline')
for i,t in enumerate(hero_head): txt((48,208+i*54),t,46,WHITE,True)
hero_body=['Back as chief executive less than two','weeks after his ouster, he eases fears','across the AI chip supply chain.']
checked_lines(hero_body,22,False,620,'hero body')
for i,t in enumerate(hero_body): txt((48,322+i*29),t,22,'#F7E8E6')

# Chip illustration, bars and crisp circuit board traces
bar_col = '#451714'
for center, top, name, figure in [(700, 312, 'KOSPI', '+6%'), (778, 270, 'TAIWAN STOCKS', '+9%')]:
    rect((center-23, top, center+23, 400), bar_col)
    rect((center-23, top, center+23, top+5), '#FFC46B')
    txt((center, top-64), name, 21, '#FFC46B', True, anchor='mm')
    txt((center, top-30), figure, 36, '#FFC46B', True, anchor='mm')

rect((860,253,958,351),'#5E1B18',outline='#3F1210',width=3,radius=13)
rect((876,269,942,335),'#5E1B18',outline='#D98E4A',width=2,radius=5)
# evenly spaced pins on each edge
for q in range(4):
    p=873+18*q
    line([(p,245),(p,253)],'#E4A15A',3); line([(p,351),(p,359)],'#E4A15A',3)
    line([(852,273+18*q),(860,273+18*q)],'#E4A15A',3)
# traces to the right, crisp stepped paths and terminal dots
for y,end_y in [(273,256),(291,285),(309,323),(327,350)]:
    line([(958,y),(966,y)],'#E4A15A',3)
    x0=966; xm=978; xe=996
    line([(x0,y),(xm,y),(xm,end_y),(xe,end_y)],'#D98E4A',2)
    ellipse((xe-3,end_y-3,xe+3,end_y+3),'#FFC46B')

cards=[
 dict(label='DEFENCE · SEOUL',color='#C4502B',icon='jets',head=['F-15Ks Scramble', 'In Response'],body=['About five Russian military aircraft', 'entered the KADIZ by Ulleung Island.']),
 dict(label='CONFLICT · UKRAINE',color='#5B6FA6',icon='barrage',head=['Russian Strike', 'Kills 2, Wounds 22'],accent=[(1,'Kills ', '2', ', Wounds ', '22')],body=['The strike on Zaporizhzhia left', 'two children among the wounded.']),
 dict(label='DISASTER · HANOI',color='#B23A48',icon='blast',head=['Hanoi Food-Shop Blast','Kills 6, Injures 10'],accent=[(1,'Kills ', '6', ', Injures ', '10')],body=['A gas blast wrecked a Dong Da', 'food shop at 8 a.m., police say.']),
 dict(label='LAW · THE HAGUE',color='#7A4FA3',icon='scales',head=['Japan Brings Forward','Its Full 2027 ICC Dues'],accent=[(1,'Its Full ', '2027', ' ICC Dues')],body=['Will pay full 2027 dues by year-end.', 'Top contributor: ~15% of ICC budget.']),
 dict(label='POLITICS · BAGHDAD',color='#A87B12',icon='pumpjack',head=['Iraq PM Orders Seizure of', 'Border Posts & Oil Fields'],body=["The order targets Kurdistan's", 'border posts and oil fields.']),
 dict(label='POLITICS · DHAKA',color='#2E7D4F',icon='plane',head=['Hasina to Fly Home','on December 16'],accent=[(1,'on ', 'December 16')],body=['India exile: plans state airline return.', 'If back, she faces a death sentence.']),
]

def draw_icon(kind,x,y,c):
    # All icon coordinates fit a 72x72 box; strokes are bold and deliberately simple.
    if kind=='jets':
        line([(x+36,y+4),(x+30,y+32),(x+10,y+44),(x+11,y+49),(x+32,y+43),(x+34,y+60),(x+26,y+66),(x+26,y+69),(x+36,y+66),(x+46,y+69),(x+46,y+66),(x+38,y+60),(x+40,y+43),(x+61,y+49),(x+62,y+44),(x+42,y+32),(x+36,y+4)],c,3)
        for a in range(0,5): line([(x+8+a*5,y+61-a*2),(x+10+a*5,y+59-a*2)],c,2)
    elif kind=='barrage':
        rect((x+12,y+8,x+60,y+67),None,outline=c,width=3)
        for yy in (17,29,41,53):
            for xx in (20,32,44):
                if (xx,yy)==(44,41):
                    line([(x+xx,y+yy),(x+xx+8,y+yy+8)],'#FFFFFF',2); line([(x+xx+8,y+yy),(x+xx,y+yy+8)],'#FFFFFF',2)
                else: rect((x+xx,y+yy,x+xx+5,y+yy+5),c)
    elif kind=='blast':
        rect((x+11,y+34,x+61,y+66),WHITE,outline=c,width=3)
        rect((x+18,y+43,x+31,y+65),WHITE,outline=c,width=2)
        ellipse((x+26,y+53,x+28,y+55),c)
        rect((x+37,y+43,x+54,y+56),WHITE,outline=c,width=2)
        line([(x+45,y+44),(x+45,y+55)],c,2)
        for stripe in range(7):
            top = x+15+stripe*6
            bottom = x+8+stripe*8
            points = [(top,y+22),(top+6,y+22),(bottom+8,y+36),(bottom,y+36)]
            d.polygon([box(point) for point in points],fill=c if stripe%2==0 else WHITE)
        line([(x+8,y+36),(x+15,y+22),(x+57,y+22),(x+64,y+36),(x+8,y+36)],c,2)
        # starburst above roof
        for dx,dy in [(0,-8),(0,8),(-8,0),(8,0),(-6,-6),(6,6),(-6,6),(6,-6)]:
            line([(x+36,y+10),(x+36+dx,y+10+dy)],c,3)
    elif kind=='scales':
        line([(x+36,y+8),(x+36,y+59),(x+19,y+66),(x+53,y+66)],c,4)
        line([(x+15,y+20),(x+57,y+20)],c,4); ellipse((x+32,y+13,x+40,y+21),c)
        for xx in (x+21,x+51):
            line([(xx,y+20),(xx-8,y+43)],c,2); line([(xx,y+20),(xx+8,y+43)],c,2)
            line([(xx-10,y+44),(xx+10,y+44)],c,3); line([(xx-9,y+44),(xx,y+53),(xx+9,y+44)],c,3)
    elif kind=='pumpjack':
        line([(x+13,y+65),(x+59,y+65)],c,4)
        line([(x+22,y+64),(x+31,y+31),(x+43,y+64)],c,4)
        line([(x+18,y+33),(x+53,y+20),(x+60,y+23)],c,5)
        line([(x+57,y+21),(x+64,y+28),(x+61,y+38),(x+55,y+39)],c,4)
        line([(x+55,y+39),(x+51,y+46)],c,3)
        line([(x+31,y+31),(x+49,y+23)],c,3)
    elif kind=='plane':
        line([(x+8,y+37),(x+37,y+34),(x+63,y+15),(x+66,y+18),(x+52,y+38),(x+66,y+50),(x+63,y+53),(x+37,y+42),(x+8,y+40),(x+8,y+37)],c,3)
        # curved return arrow beneath
        line([(x+18,y+58),(x+27,y+66),(x+45,y+66),(x+56,y+58)],c,3)
        line([(x+50,y+58),(x+56,y+58),(x+56,y+64)],c,3)

for i,card in enumerate(cards):
    x=28+(i%2)*496; y=423+(i//2)*186; c=card['color']
    rect((x,y,x+472,y+182),WHITE,outline='#D9D2C2',width=1,radius=10)
    rect((x,y,x+8,y+182),c)
    # category chip
    cw=width(card['label'],17,True)+18
    rect((x+26,y+9,x+26+cw,y+34),c,radius=4)
    txt((x+35,y+11),card['label'],17,WHITE,True)
    draw_icon(card['icon'],x+384,y+12,c)
    checked_lines(card['head'],28,True,358,f'card {i+1} headline')
    for j,t in enumerate(card['head']):
        yy=y+37+j*32
        accent=next((a for a in card.get('accent',[]) if a[0]==j),None)
        if accent:
            pieces=accent[1:]; cx=x+26
            for k,piece in enumerate(pieces):
                col=c if k%2==1 else INK
                txt((cx,yy),piece,28,col,True); cx+=width(piece,28,True)
        else: txt((x+26,yy),t,28,INK,True)
    checked_lines(card['body'],26,False,432,f'card {i+1} body')
    for j,t in enumerate(card['body']): txt((x+26,y+102+j*31),t,26,BODY)

# Footer
rect((0,982,1024,1024),NAVY)
txt((976,993),'Sources: Reuters · Yonhap · CNA',20,'#C9D4E2',anchor='ra')

out=Path(os.environ.get('MAKEFUN_OUTPUT_DIR',Path(__file__).resolve().parent))
out.mkdir(parents=True,exist_ok=True)
final=im.resize((1024,1024),Image.Resampling.LANCZOS)
final.save(out/'entry.png',format='PNG',optimize=True)
final.resize((300,300),Image.Resampling.LANCZOS).save(out/'preview300.png',format='PNG',optimize=True)
print(f'Width assertions passed; wrote {out / "entry.png"}')



def create_cover_page(brief, cover_logo):
    brief.add_page()
    brief.set_fill_color(252, 203, 181)
    brief.set_text_color(60, 60, 60)
    brief.set_font('montserrat', size=48)
    brief.rect(x=10, y=10, w=275, h=190, style='F')
    brief.image(str(cover_logo), x=20, y=90, w=100)
    brief.set_xy(20, 110)
    brief.set_font('nexa', size=16)
    brief.cell(w=0, txt='beyond visuals')
    brief.set_xy(20, 185)
    brief.set_font('nexa', size=14)
    brief.cell(0, txt='www.animotions.be')

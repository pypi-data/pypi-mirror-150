from markdown import markdown

def joke():
    return markdown(u'Wenn ist das Nunst\u00fcck git und Slotermeyer?'
                    u'Ja! ... **Beiherhund** das Oder die Flipperwaldt '
                    u'gersput.')

def joke2():
    return (u'Wenn ist das Nunst\u00fcck git und Slotermeyer? Ja! ... ')
            
def helloworld(name):
    print(f"Hello {name}")
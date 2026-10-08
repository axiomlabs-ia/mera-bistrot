#!/usr/bin/env python3
"""
Aggiunge lo spagnolo a menu-dati.js: accanto a ogni `it`/`en` mette `es`,
accanto a ogni `dit`/`den` mette `des`.

    python3 aggiungi-spagnolo.py

Si puo' rilanciare: le voci che hanno gia' `es` vengono saltate.
Quello che non e' nel dizionario resta in italiano (giusto per i nomi propri:
Margherita, Negroni, Caprese) e viene elencato a fine esecuzione per controllo.
"""
import pathlib
import re
import sys

NOMI = {
    # sezioni e gruppi
    'Colazione': 'Desayuno', 'Dolci': 'Dulces', 'Salate': 'Saladas',
    'Formule colazione': 'Fórmulas desayuno', 'Caffetteria': 'Cafetería',
    'Al banco': 'En la barra', 'Cornetti e dolci da forno': 'Bollería',
    'Centrifughe': 'Zumos naturales', 'Antipasti': 'Entrantes',
    'Primi piatti': 'Primeros', 'Secondi e contorni': 'Segundos y guarniciones',
    'Secondi': 'Segundos', 'Contorni': 'Guarniciones',
    'Insalatone e hamburger': 'Ensaladas y hamburguesas', 'Insalatone': 'Ensaladas',
    'Hamburger': 'Hamburguesas', 'Focacce e pizze tonde': 'Focaccias y pizzas',
    'Le nostre focacce': 'Nuestras focaccias', 'Pizze tonde rosse': 'Pizzas rojas',
    'Pizze tonde bianche': 'Pizzas blancas', 'Aperitivo': 'Aperitivo',
    'Cocktail': 'Cócteles', 'Bevande': 'Bebidas', 'Pizza al taglio': 'Pizza al corte',
    'TUTTO IL GIORNO': 'TODO EL DÍA',
    'TUTTO IL GIORNO · MERULANA 108': 'TODO EL DÍA · MERULANA 108',
    'Tutti i giorni 7:30 — 22:00': 'Todos los días 7:30 — 22:00',
    'Servita fino alle 16:00, anche nel pomeriggio.':
        'Servido hasta las 16:00, también por la tarde.',
    'Ogni formula comprende una bevanda a scelta: cocktail classico, spritz, vino, birra o analcolica.':
        'Cada fórmula incluye una bebida a elegir: cóctel clásico, spritz, vino, cerveza o refresco.',
    'Due porte più in là, al 108. Prezzo al trancio. Pizze tonde da asporto su ordinazione.':
        'Dos puertas más allá, en el 108. Precio por porción. Pizzas redondas para llevar por encargo.',

    # colazione
    'Macedonia di frutta': 'Macedonia de frutas', 'Waffle': 'Gofre',
    'Porridge': 'Porridge', 'Pancake': 'Tortitas', 'Bowl di yogurt': 'Bol de yogur',
    'Toast cotto': 'Tostado de jamón cocido', 'Toast crudo': 'Tostado de jamón serrano',
    'Toast al salmone': 'Tostado de salmón',
    'Uova strapazzate con bacon': 'Huevos revueltos con bacon',
    'Uova strapazzate con würstel': 'Huevos revueltos con salchichas',
    'Omelette vegetariana': 'Tortilla vegetariana',
    'Omelette classica': 'Tortilla clásica',
    'Maxi club sandwich classic': 'Maxi club sandwich',
    'All’Italiana': 'A la italiana', 'Dolce': 'Dulce', 'Salata': 'Salada',
    'Maxi club sandwich': 'Maxi club sandwich', 'Macedonia': 'Macedonia',

    # caffetteria
    'Caffè': 'Café', 'Caffè decaffeinato': 'Café descafeinado',
    'Caffè latte': 'Café con leche', 'Caffè freddo': 'Café frío',
    'Caffè corretto': 'Carajillo', 'Caffè doppio': 'Café doble',
    'Latte bianco': 'Leche caliente', 'Cappuccino': 'Capuchino',
    'Cappuccino freddo': 'Capuchino frío',
    'Cappuccino deca o senza lattosio': 'Capuchino descafeinado o sin lactosa',
    'Cappuccino orzo o ginseng': 'Capuchino de cebada o ginseng',
    'Cappuccino grande': 'Capuchino grande',
    'Orzo piccolo': 'Cebada, pequeño', 'Orzo grande': 'Cebada, grande',
    'Ginseng piccolo': 'Ginseng, pequeño', 'Ginseng grande': 'Ginseng, grande',
    'Americano grande': 'Americano grande', 'Tè caldo': 'Té caliente',
    'Crema di caffè': 'Crema de café', 'Cioccolata calda': 'Chocolate caliente',
    'Cornetti mignon': 'Mini cruasanes', 'Cornetto classico': 'Cruasán clásico',
    'Cornetti farciti': 'Cruasanes rellenos',
    'Ciambelle e bombe classiche': 'Donuts clásicos',
    'Ciambelle e bombe farcite': 'Donuts rellenos', 'Ciambellone': 'Bizcocho',
    'Crostata': 'Tarta de mermelada', 'Torta del giorno': 'Tarta del día',
    'Dissetante': 'Refrescante', 'Drenante': 'Drenante', 'Depurativa': 'Depurativa',
    'Detox': 'Detox', 'A scelta': 'A tu gusto',

    # antipasti
    'Supplì al telefono': 'Supplì clásico', 'Crocchetta di patate': 'Croqueta de patata',
    'Supplì alla carbonara': 'Supplì a la carbonara',
    'Supplì all’amatriciana': 'Supplì a la amatriciana',
    'Bruschetta al pomodoro': 'Bruschetta de tomate',
    'Bruschetta al pesto': 'Bruschetta al pesto',
    'Bruschetta stracciatella e alici': 'Bruschetta de stracciatella y anchoas',
    'Bruschetta salmone e stracciatella': 'Bruschetta de salmón y stracciatella',
    'Tris di bruschette': 'Trío de bruschettas',
    'Crudo e bufala': 'Jamón serrano y mozzarella de búfala',
    'Tagliere di salumi': 'Tabla de embutidos',

    # primi
    'Tonnarelli alla carbonara': 'Tonnarelli a la carbonara',
    'Tonnarelli all’amatriciana': 'Tonnarelli a la amatriciana',
    'Tonnarelli cacio e pepe': 'Tonnarelli cacio e pepe',
    'Tonnarelli alla gricia': 'Tonnarelli a la gricia',
    'Penne al pomodoro e basilico': 'Penne con tomate y albahaca',
    'Lasagna alla bolognese': 'Lasaña a la boloñesa',
    'Fettuccine al ragù di manzo': 'Fettuccine con ragú de ternera',
    'Fettuccine ai funghi porcini': 'Fettuccine con boletus',
    'Fettuccine al salmone': 'Fettuccine con salmón',

    # secondi e contorni
    'Polpette al sugo': 'Albóndigas en salsa de tomate',
    'Polpette all’amatriciana': 'Albóndigas a la amatriciana',
    'Polpette ai funghi porcini': 'Albóndigas con boletus',
    'Polpette al ragù': 'Albóndigas al ragú',
    'Hamburger al piatto': 'Hamburguesa sin pan',
    'Cotoletta di pollo': 'Escalope de pollo',
    'Thai di pollo con verdure': 'Pollo thai con verduras',
    'Tagliata di pollo': 'Pollo en tiras',
    'Patate al forno': 'Patatas al horno', 'Patatine fritte': 'Patatas fritas',
    'Cicoria alla romana': 'Achicoria a la romana', 'Scarola': 'Escarola',
    'Broccoli': 'Brócoli',

    # insalatone e hamburger
    'Classica': 'Clásica', 'Caesar': 'César', 'Salmone': 'Salmón',
    'Classico': 'Clásica', 'Formula hamburger': 'Fórmula hamburguesa',

    # focacce e pizze
    'Mortadella & stracciatella': 'Mortadela y stracciatella',
    'Crudo & stracciatella': 'Jamón serrano y stracciatella',
    'Salmone & bufala': 'Salmón y mozzarella de búfala',
    'La vegetariana': 'La vegetariana',
    'Margherita con prosciutto cotto': 'Margherita con jamón cocido',
    'Margherita con funghi': 'Margherita con champiñones',
    'Würstel e patatine': 'Salchichas y patatas fritas', 'Napoli': 'Nápoles',
    'Bufala e pachino': 'Búfala y tomate cherry',
    'Patate e salsiccia': 'Patata y salchicha',
    'Fiori e alici': 'Flor de calabacín y anchoas',
    'Vegetariana': 'Vegetariana',
    'Porcini, provola e salsa marinara': 'Boletus, provola y salsa marinara',
    'Cesare': 'César', 'Formula pizza': 'Fórmula pizza',

    # cocktail
    'Caipiroska alla fragola': 'Caipiroska de fresa',

    # bevande
    'Acqua 0,5 L': 'Agua 0,5 L', 'Acqua 0,75 L': 'Agua 0,75 L',
    'Succhi di frutta': 'Zumos de fruta',
    'Tè alla pesca o limone': 'Té de melocotón o limón',
    'Tè della casa': 'Té de la casa',
    'Spremuta d’arancia': 'Zumo de naranja natural',
    'Spremuta di pompelmo': 'Zumo de pomelo natural',
    'Schweppes limone': 'Schweppes limón', 'Schweppes tonica': 'Schweppes tónica',
    'Campari Soda corretto': 'Campari Soda con licor',
    'Ichnusa non filtrata': 'Ichnusa sin filtrar',
    'Birra alla spina': 'Cerveza de barril',
    'Calice di Prosecco': 'Copa de Prosecco',
    'Calice di vino bianco': 'Copa de vino blanco',
    'Calice di vino rosso': 'Copa de vino tinto', 'Amari': 'Amaro',

    # al taglio
    'Bianca': 'Blanca', 'Rossa, Marinara, Patate': 'Roja, Marinara, Patata',
    'Speciali': 'Especiales', 'Ripiene': 'Rellenas',
    'Bibita in lattina': 'Refresco en lata',
}

DESCRIZIONI = {
    'Nutella o sciroppo d’acero, frutta fresca': 'Nutella o sirope de arce, fruta fresca',
    'Fiocchi d’avena cotti in acqua o latte, con frutta fresca':
        'Copos de avena cocidos en agua o leche, con fruta fresca',
    'Yogurt cremoso con granola e frutta fresca':
        'Yogur cremoso con granola y fruta fresca',
    'Prosciutto cotto, insalata e bufala':
        'Jamón cocido, lechuga y mozzarella de búfala',
    'Prosciutto crudo, insalata e stracciatella':
        'Jamón serrano, lechuga y stracciatella',
    'Salmone affumicato, crema al formaggio e avocado':
        'Salmón ahumado, queso crema y aguacate',
    'Pane bruscato e insalata': 'Pan tostado y ensalada',
    'Uova, zucchine, parmigiano': 'Huevo, calabacín y parmesano',
    'Uova, prosciutto cotto, cheddar e bacon':
        'Huevo, jamón cocido, cheddar y bacon',
    'Pane tostato, prosciutto cotto, uova, bacon croccante, lattuga, pomodoro, maionese, cheddar':
        'Pan tostado, jamón cocido, huevo, bacon crujiente, lechuga, tomate, mayonesa y cheddar',
    'Torta del giorno o crostata + spremuta d’arancia + caffè o cappuccino':
        'Tarta del día o tarta de mermelada + zumo de naranja + café o capuchino',
    'Dolce a scelta + spremuta d’arancia + caffè o cappuccino':
        'Un dulce a elegir + zumo de naranja + café o capuchino',
    'Colazione salata a scelta (escluso maxi club sandwich) + spremuta + caffè o cappuccino':
        'Un salado a elegir (maxi club sandwich excluido) + zumo + café o capuchino',
    'Spremuta d’arancia + caffè o cappuccino': 'Zumo de naranja + café o capuchino',
    'Crema, albicocca, visciole, cioccolato': 'Crema, albaricoque, guinda, chocolate',
    'Pistacchio, albicocca, visciole, cioccolato e frutta':
        'Pistacho, albaricoque, guinda, chocolate y fruta',
    'Mela, limone, zenzero': 'Manzana, limón, jengibre',
    'Pompelmo, cetriolo, finocchio': 'Pomelo, pepino, hinojo',
    'Kiwi, sedano, melone, zenzero': 'Kiwi, apio, melón, jengibre',
    'Carota, mango, arancia': 'Zanahoria, mango, naranja',
    'Carota, sedano, finocchio': 'Zanahoria, apio, hinojo',
    'Con 3 frutti della lista': 'Con 3 frutas de la lista',
    '2 pezzi': '2 piezas',
    'Con pomodorini confit · 2 pezzi': 'Con tomates confitados · 2 piezas',
    'Accompagnati da una focaccia': 'Acompañados de una focaccia',
    'Con 2 focacce e mozzarella di bufala, per due persone':
        'Con 2 focaccias y mozzarella de búfala, para dos personas',
    'Morbide polpette di manzo nel sugo di pomodoro · 5 pezzi':
        'Albóndigas tiernas de ternera en salsa de tomate · 5 piezas',
    'Polpette di manzo con guanciale in salsa all’amatriciana · 5 pezzi':
        'Albóndigas de ternera con guanciale en salsa amatriciana · 5 piezas',
    'Polpette di manzo in salsa ai funghi porcini · 5 pezzi':
        'Albóndigas de ternera en salsa de boletus · 5 piezas',
    'Morbide polpette con salsa al ragù · 5 pezzi':
        'Albóndigas tiernas con salsa de ragú · 5 piezas',
    'Pomodori confit, grana, salsa all’aceto balsamico':
        'Tomates confitados, grana y salsa de vinagre balsámico',
    'Lattuga, rughetta, pomodorini confit, tonno, olive nere, noci':
        'Lechuga, rúcula, tomates confitados, atún, aceitunas negras y nueces',
    'Lattuga, pomodorini, cetrioli, carote, cipolla rossa, olive nere':
        'Lechuga, tomate cherry, pepino, zanahoria, cebolla roja y aceitunas negras',
    'Lattuga, pollo grigliato, crostini, scaglie di grana, salsa Caesar':
        'Lechuga, pollo a la plancha, picatostes, lascas de grana y salsa César',
    'Lattuga, salmone affumicato, avocado, cetrioli, pomodorini, semi di sesamo, salsa teriyaki':
        'Lechuga, salmón ahumado, aguacate, pepino, tomate cherry, sésamo y salsa teriyaki',
    'Hamburger di manzo, lattuga, pomodoro, pane morbido + patatine fritte':
        'Hamburguesa de ternera, lechuga, tomate, pan brioche + patatas fritas',
    'Hamburger di manzo, cheddar, lattuga, pomodoro, pane morbido + patatine fritte':
        'Hamburguesa de ternera, cheddar, lechuga, tomate, pan brioche + patatas fritas',
    'Hamburger di manzo, cheddar, bacon croccante, lattuga, pomodoro, pane morbido + patatine fritte':
        'Hamburguesa de ternera, cheddar, bacon crujiente, lechuga, tomate, pan brioche + patatas fritas',
    'Hamburger a scelta + contorno + bevanda':
        'Hamburguesa a elegir + guarnición + bebida',
    'Mortadella, stracciatella, granella di pistacchio':
        'Mortadela, stracciatella y pistacho picado',
    'Prosciutto crudo, stracciatella, pesto': 'Jamón serrano, stracciatella y pesto',
    'Salmone, bufala, rucola': 'Salmón, mozzarella de búfala y rúcula',
    'Scarola, broccoli, bufala': 'Escarola, brócoli y mozzarella de búfala',
    'Pomodoro, aglio, origano, olio EVO': 'Tomate, ajo, orégano y aceite de oliva',
    'Pomodoro, mozzarella, basilico': 'Tomate, mozzarella y albahaca',
    'Pomodoro, mozzarella, würstel, patatine fritte':
        'Tomate, mozzarella, salchichas y patatas fritas',
    'Pomodoro, mozzarella, alici, origano': 'Tomate, mozzarella, anchoas y orégano',
    'Pomodoro, mozzarella, salame piccante': 'Tomate, mozzarella y salami picante',
    'Pomodoro, mozzarella, prosciutto cotto, funghi, olive, carciofi':
        'Tomate, mozzarella, jamón cocido, champiñones, aceitunas y alcachofas',
    'Pomodoro, mozzarella di bufala, pomodorini, basilico':
        'Tomate, mozzarella de búfala, tomate cherry y albahaca',
    'Pomodoro, mozzarella, guanciale, pecorino, pepe':
        'Tomate, mozzarella, guanciale, pecorino y pimienta',
    'Mozzarella, prosciutto cotto': 'Mozzarella y jamón cocido',
    'Mozzarella, funghi, salsiccia': 'Mozzarella, champiñones y salchicha',
    'Mozzarella, fiori di zucca, alici': 'Mozzarella, flor de calabacín y anchoas',
    'Crema di pecorino, pepe nero': 'Crema de pecorino y pimienta negra',
    'Mozzarella, verdure miste': 'Mozzarella y verduras variadas',
    'Mozzarella, guanciale, crema all’uovo, pecorino, pepe':
        'Mozzarella, guanciale, crema de huevo, pecorino y pimienta',
    'Mozzarella, pollo grigliato, lattuga, salsa Caesar, grana':
        'Mozzarella, pollo a la plancha, lechuga, salsa César y grana',
    'Pizza a scelta + supplì o crocchetta di patate + bibita (lattina o acqua)':
        'Pizza a elegir + supplì o croqueta de patata + bebida (lata o agua)',
    'Pizza al taglio e una bevanda': 'Pizza al corte y una bebida',
    'Selezione di fritti caldi: supplì al telefono, crocchetta di patate, supplì carbonara o amatriciana':
        'Selección de fritos calientes: supplì clásico, croqueta de patata, supplì carbonara o amatriciana',
    'Tagliere misto di salumi, stuzzichini e pizza al taglio':
        'Tabla mixta de embutidos, aperitivos y pizza al corte',
    'Tagliere misto di salumi e formaggi, olive, sottoli, con una focaccia vuota':
        'Tabla mixta de embutidos y quesos, aceitunas, encurtidos y una focaccia',
    'Aperol, prosecco, soda, arancia': 'Aperol, prosecco, soda y naranja',
    'Campari, prosecco, soda, arancia': 'Campari, prosecco, soda y naranja',
    'Prosecco, sciroppo di sambuco, soda, menta, lime':
        'Prosecco, sirope de saúco, soda, menta y lima',
    'Limoncello, prosecco, soda, limone': 'Limoncello, prosecco, soda y limón',
    'Prosecco, liquore al frutto della passione, soda, frutta fresca':
        'Prosecco, licor de maracuyá, soda y fruta fresca',
    'Prosecco, purea di pesca': 'Prosecco y puré de melocotón',
    'Rum bianco, zucchero di canna, lime, menta, soda':
        'Ron blanco, azúcar de caña, lima, menta y soda',
    'Prosecco, succo d’arancia': 'Prosecco y zumo de naranja',
    'Rum scuro, cola, lime': 'Ron oscuro, cola y lima',
    'Vodka, zucchero di canna, lime': 'Vodka, azúcar de caña y lima',
    'Vodka, lime, zucchero di canna, fragole fresche':
        'Vodka, lima, azúcar de caña y fresas frescas',
    'Gin, vermouth rosso, Campari': 'Ginebra, vermut rojo y Campari',
    'Prosecco, vermouth rosso, Campari': 'Prosecco, vermut rojo y Campari',
    'Campari, vermouth rosso, soda': 'Campari, vermut rojo y soda',
    'Gin, acqua tonica, lime o limone': 'Ginebra, tónica y lima o limón',
    'Vodka, ginger beer, succo di lime': 'Vodka, ginger beer y zumo de lima',
    'Vodka, Baileys': 'Vodka y Baileys',
    'Malibu, cola, lime': 'Malibu, cola y lima',
    'Energy drink, Zero, Pink Edition': 'Energy drink, Zero, Pink Edition',
    'Heineken o Moretti': 'Heineken o Moretti',
    # note di sezione
    'Servita fino alle 16:00, anche nel pomeriggio.':
        'Servido hasta las 16:00, también por la tarde.',
    'Ogni formula comprende una bevanda a scelta: cocktail classico, spritz, vino, birra o analcolica.':
        'Cada fórmula incluye una bebida a elegir: cóctel clásico, spritz, vino, cerveza o refresco.',
    'Due porte più in là, al 108. Prezzo al trancio. Pizze tonde da asporto su ordinazione.':
        'Dos puertas más allá, en el 108. Precio por porción. Pizzas redondas para llevar por encargo.',
}


def aggiungi(testo, motivo, tabella, nuova_chiave, mancanti):
    """Il motivo deve catturare anche l'eventuale chiave spagnola gia' presente
    (ultimo gruppo): senza, al secondo giro la guardia non la vedrebbe e la
    aggiungerebbe una seconda volta."""
    def sostituisci(m):
        intero, italiano, gia = m.group(0), m.group(1), m.groups()[-1]
        if gia:
            return intero                       # gia' tradotto: non si tocca
        spagnolo = tabella.get(italiano)
        if spagnolo is None:
            mancanti.append(italiano)
            spagnolo = italiano                 # nomi propri: restano cosi'
        return f"{intero}, {nuova_chiave}: '{spagnolo}'"
    return re.sub(motivo, sostituisci, testo)


def main():
    p = pathlib.Path(__file__).parent / 'menu-dati.js'
    if not p.exists():
        sys.exit('menu-dati.js non trovato')
    s = p.read_text(encoding='utf-8')
    mancanti = []
    s = aggiungi(s, r"it: '([^']*)',\s*\n?\s*en: '[^']*'(,\s*es: '[^']*')?",
                 NOMI, 'es', mancanti)
    s = aggiungi(s, r"dit: '([^']*)',\s*\n?\s*den: '[^']*'(,\s*des: '[^']*')?",
                 DESCRIZIONI, 'des', mancanti)
    p.write_text(s, encoding='utf-8')

    print(f"aggiunte {s.count(chr(39) + ', es: ') + s.count(', es: ')} voci spagnole")
    senza = sorted(set(mancanti))
    if senza:
        print(f'\nlasciate in italiano ({len(senza)}) — verifica se vanno tradotte:')
        for v in senza:
            print(f'  · {v}')


if __name__ == '__main__':
    main()

#from __future__ import unicode_literals
from flask import Flask, render_template, request


APP_NAME = "Keg's List"

app = Flask(__name__)
    
@app.route('/home')
@app.route('/')
def home():
    return render_template('index.html', page_title = APP_NAME)

@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        query_string = request.form.get("query_string")
        user = request.form.get("user", None)
        expansion = request.form.get("expansion", 0)
        sort = []
        if request.form.get("overall"):
            sort.append("overall")
        if request.form.get("appearance"):
            sort.append("appearance")
        if request.form.get("taste"):
            sort.append("taste")
        if request.form.get("palate"):
            sort.append("palate")
        if request.form.get("aroma"):
            sort.append("aroma")
        
        print_debug = query_string + " " + str(user) + " " + str(expansion) + " " + str(sort) 
        
        page_title = query_string + " - " + APP_NAME + " Search"

        query_result = {'list':[]}
        # query_result = query(query_string, sort_by=sort_by, user=user, expansion=expansion)
        if 'list' in query_result:
            # beers_tuples = query_result['list']
            # dummy search results
            beers_tuples = [('Summer Honey Surprise', 0.43570055421261522, '72817'),
                ('California Pale Ale (CPA)', 0.34620041694131759, '6038'),
                ('Centennial Pale Ale', 0.3326512714420391, '75449'),
                ('Cascadian Dark Ale', 0.32208447436592719, '68447'),
                ('Zvikovsky Pale Ale 15\xc2\xb0', 0.318908241776509, '73845'),
                ('Amarillo Single Hop Pale Ale', 0.3097586440115308, '65636'),
                ('Deceiver', 0.29880681872391268, '74672'),
                ('Ghost Ale', 0.29515260406523697, '30231'),
                ('Biere Blonde', 0.29371090922826593, '63736'),
                ('Hakusekikan White Ale', 0.29179652546850726, '45372')]
            
            beers = [{'name': name.decode('utf-8'), 'score': score} for (name,score,beer_id) in beers_tuples]
                
            return render_template("search.html", page_title = page_title, query_string=query_string, 
                beers=beers)
        elif 'beer' in query_result:
            # beer_list = query_result['beer']
            # dummy beer info
            beer_list = ['Ghost Ale',
                3.5,
                3.5,
                4.0,
                3.5,
                4.0,
                0.66325380239035947,
                ['Dopple Weizen',
                "Dragon's Milk",
                'TBonz Blond Bombshell',
                'Instigator Doppelbock',
                'Expresso Vanilla Porter',
                'Wisnia W Piwie',
                "Rudolph's Raspberry Yuletide",
                'Triple Play',
                'Mocha Vanilla Stout',
                'Black Beer'],
                [u'gingeri',
                u'grapefruit',
                u'refreshingli',
                u'graviti',
                u'lurk',
                u'quench',
                u'citru',
                u'floweri',
                u'md',
                u'dri']]
            
            beer = {'name':beer_list[0], 'similarity':beer_list[6], 'similar_beers':beer_list[7], 'top_terms':beer_list[8]}
            
            return render_template("profile.html", page_title = page_title, query_string=query_string, 
                beer=beer)
                
    return render_template("search.html", page_title = APP_NAME)

#    @app.route('/show/<beer_name>')
#    def show(beer_name):
#        
#        return render_template("profile.html", page_title = beer_name, beer=beer)


if __name__ == '__main__':
    app.run(debug=True)
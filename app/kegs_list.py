from flask import Flask, render_template, request
from tf_idf_index import dd, ll
import data_loader


APP_NAME = "Keg's List"

ENGINE = data_loader.main()

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

        query_result = ENGINE.query(query_string, sort_by=sort_by, user=user, expansion=expansion)

        if 'list' in query_result:
            beers_tuples = query_result['list']
            
            beers = [{'name': name.decode('utf-8'), 'score': score} for (name,score,beer_id) in beers_tuples]
                
            return render_template("search.html", page_title = page_title, query_string=query_string, 
                beers=beers)
        elif 'beer' in query_result:
            beer_list = query_result['beer']
            
            beer = {'name':beer_list[0], 'appearance':beer_list[1], 'aroma':beer_list[2], 'overall':beer_list[3], 'palate':beer_list[4], 'taste':beer_list[5], 
            'similarity':beer_list[6], 'similar_beers':beer_list[7], 'top_terms':beer_list[8]}
            
            return render_template("profile.html", page_title = page_title, query_string=query_string, 
                beer=beer)
                
    return render_template("search.html", page_title = APP_NAME)

#    @app.route('/show/<beer_name>')
#    def show(beer_name):
#        
#        return render_template("profile.html", page_title = beer_name, beer=beer)


if __name__ == '__main__':
    app.run(debug=True)
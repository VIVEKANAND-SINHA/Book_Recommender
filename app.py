from flask import Flask,render_template,request,jsonify
import pickle
import numpy as np

# from requests import request

popular_df = pickle.load(open('popular.pkl','rb'))
books = pickle.load(open('books.pkl','rb'))
pt = pickle.load(open('pt.pkl','rb'))
finalbooks = pickle.load(open('finalbooks.pkl','rb'))
simlilartiy_scores = pickle.load(open('simlilartiy_scores.pkl','rb'))
app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html",
                           book_name =list(popular_df["Book-Title"].values),
                           author = list(popular_df["Book-Author"].values),
                           image = list(popular_df["Image-URL-M"].values),
                           votes =list(popular_df["num_ratings"].values),
                           rating = list(popular_df["avg_ratings"].values))

@app.route('/recommend')
def recommend():
    book_list = finalbooks['Book-Title'].values
    return render_template('recommend.html',book_list=book_list)

@app.route('/recommend_books',methods=["post"])
def recommend_book():
    book_list = finalbooks['Book-Title'].values
    book_name = request.form.get('bookname')
    print(book_name)
    try:
        index = np.where(pt.index == book_name)[0][0]
        similar_items = sorted(list(enumerate(simlilartiy_scores[index])),key= lambda x:x[1],reverse = True)[1:5]
        data = []
        for i in similar_items:
            item = []
            temp_df = books[books['Book-Title']==pt.index[i[0]]]
            item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
            item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
            item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))
            
            data.append(item)
        return render_template('recommend.html',data=data,book_list=book_list) 
    except:
        return render_template('recommend.html',msg = "Error In Name",book_list=book_list)
    

if __name__ == "__main__":
    app.run(debug=True)
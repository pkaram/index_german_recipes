#data are available on kaggle
#https://www.kaggle.com/sterby/german-recipes-dataset
#download the data and place them in the working directory

import pandas as pd
from nltk.corpus import stopwords

def main():
    #import data
    recipes=pd.read_json('recipes.json')

    #there are duplicate entries for most of the recipes, we will select the most recent recipe for all cases
    month_strings={'January':1,'February':2,'March':3,'April':4,'May':5,'June':6,
                   'July':7,'August':8,'September':9,'October':10,'November':11,'December':12}
    recipes['Month']=[month_strings[s] for s in recipes['Month']]
    recipes['Year']=pd.to_numeric(recipes['Year'])
    recipes['Day']=pd.to_numeric(recipes['Day'])
    recipes['date']=pd.to_datetime(recipes[['Year','Month','Day']],format='%Y-%m-%d')
    #keep the most recent recipe update
    recipes=recipes.sort_values('date').drop_duplicates('Url',keep='last')
    #extract the number id from the url given by chefkoch, to be used as an identification key for recipes
    recipes['id']=recipes.Url.str.extract('(\d+)')
    #reset index
    recipes=recipes.reset_index(drop=True)
    #drop columns
    recipes=recipes.drop(columns=['Day','Year','Month','Weekday'])

    #get all Ingredients for all recipes
    ingredients_df=recipes[['id','Ingredients']]
    ingredients_df=ingredients_df.explode('Ingredients')

    #we will extract all ingredients regardless of the quantity they refer to
    #Some patterns to note:
    #ingredients start with capital letters, since objects start with capital letters in german language
    #there is a comma separator which separates ingredient with additional description
    #quantity of ingredient is located first before ingredient

    #join and split ingredients to identify additional patterns
    join_ing=' '.join(ingredients_df.Ingredients.values)
    join_ing=join_ing.replace(',','').replace(')','').replace('(','').replace('-','')
    split_ing=join_ing.split(' ')
    split_ing=pd.DataFrame(split_ing,columns=['terms'])
    terms=pd.DataFrame(split_ing.terms.value_counts())
    terms=terms.reset_index()
    #change the column names
    terms.columns=['terms','cnt']

    #keep only terms where the first letter is uppercase
    terms['first_letter']=[s[0] if len(s)>0 else 'a' for s in terms['terms']]
    terms['uppercase']=[s.isupper() for s in terms['first_letter']]
    terms=terms[terms['uppercase']==True]
    terms=terms.reset_index(drop=True)
    terms=terms.drop(columns=['uppercase','first_letter'])
    #filter out string cases which refer to quantities
    terms=terms[~terms['terms'].isin(['EL','TL','Pck.','Dose/n','Dose','Dosen','Für','Dressing:','Salat:'])].reset_index(drop=True)
    #we could also filter terms based on a known german food dictionary, if this was available

    #define if ingredients in ingredients_df are included in terms, if yes extract the ingredient that is assigned
    ingredients_df['ingredient']=ingredients_df['Ingredients'].str.split(' ')
    ingredients_df=ingredients_df.explode('ingredient')
    #remove all special characters that you replaced for terms
    ingredients_df['ingredient']=[s.replace(',','').replace(')','').replace('(','').replace('-','') for s in ingredients_df['ingredient']]
    ingredients_df['is_ingredient']=[(s in terms.terms.values) for s in ingredients_df['ingredient']]
    #keep only ingredients included
    ingredients_df=ingredients_df[ingredients_df.is_ingredient==True]
    ingredients_df=ingredients_df.drop_duplicates()
    ingredients_df=ingredients_df.drop(columns=['is_ingredient','Ingredients'])
    ingredients_df=ingredients_df.reset_index(drop=True)
    german_stopwords = stopwords.words('german')

    ingredients_df=ingredients_df[~(ingredients_df['ingredient'].isin(german_stopwords))]
    ingredients_df=ingredients_df.reset_index(drop=True)

    return  recipes,ingredients_df

if __name__=='__main__':
    main()

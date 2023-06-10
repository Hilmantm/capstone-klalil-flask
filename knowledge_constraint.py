import pandas as pd

# knowledge based on paper
def mood_constraint(mood):
    mood = mood.capitalize()
    preferences = []
    if mood == "Senang" or mood == "Sedih":
        preferences = ["Petualangan", "Keluarga", "Romantis", "Budaya"]
    elif mood == "Tenang" or mood == "Marah":
        preferences = ["Alam", "Hiburan", "Olahraga", "Relaksasi"]

    return preferences

def filter_by_budget(df, column_name, category):
    category = category.capitalize()
    quartiles = df[column_name].quantile([0.25, 0.5, 0.75])
    q1 = quartiles[0.25]
    q2 = quartiles[0.5]
    q3 = quartiles[0.75]

    if category == "Low":
        filtered_df = df[df[column_name] <= q1]
    elif category == "Medium":
        filtered_df = df[(df[column_name] > q1) & (df[column_name] <= q2)]
    elif category == "High":
        filtered_df = df[((df[column_name] > q2) & (df[column_name] <= q3)) | (df[column_name] > q3) ]
    elif category == "Random":
        filtered_df = df
    else:
        filtered_df = []

    return filtered_df


def filter_by_city(df, city):
    city = city.capitalize()
    filtered_df = df[df["City"] == city]
    return filtered_df


def knowledge_recommender(df, mood, budget, city):
    recommended_destinations = []

    mood_preferences = mood_constraint(mood)

    # filter dataset based on budget
    filtered_df = filter_by_budget(df, "Price", budget)

    # filter dataset based on city
    filtered_df = filter_by_city(filtered_df, city)

    # print(filtered_df)
    recommended_destinations = filtered_df[
        filtered_df["new_category"].apply(lambda x: any(preference in x for preference in mood_preferences))]

    return recommended_destinations

def give_scoring(df):
    # this function will return score for each user recommended items
    df['score'] = 1
    return df

def knowledge_data():
    df = pd.read_csv("./dataset/tourism_with_id_updated.csv")
    unused_column = ["Description", "Time_Minutes", "Coordinate"]
    df.drop(unused_column, axis=1, inplace=True)
    knowledge_recommendation = knowledge_recommender(df, 'Tenang', 'High', "Bandung")
    knowledge_recommendation.sort_values("Rating", ascending=False, inplace=True)
    dropped_column = ["Place_Name", "City", "Price", "Lat", "Long", "new_category", "Rating"]
    knowledge_recommendation.drop(dropped_column, axis=1, inplace=True)
    knowledge_recommendation = give_scoring(knowledge_recommendation)
    return knowledge_recommendation
import streamlit as st
import pickle

laptops = pickle.load(open('df.pkl', 'rb'))
sig = pickle.load(open('sig.pkl', 'rb'))

st.set_page_config(page_title='Laptop Recommendation System', page_icon='💻')

menu = ["Home", "About"]
choice = st.sidebar.selectbox("Menu", menu)

if choice == "Home":
    st.header('Laptop Recommendation System')
    nav3, nav4 = st.columns([1, 1])
    with nav3:
        value1 = st.number_input('Minimum Price',step=5000)
    with nav4:
        value2 = st.number_input('Maximum Price',value=300000,step=5000)

    PriceCheck = laptops[laptops['price'].between(value1, value2)]
    search_list = ['Brand and Model', 'Specifications']

    # values = st.slider(
    #      'Select a price range',
    #     0, 300000, (0, 300000))
    # if st.button('Apply Filter'):
    #     st.write(values)
    #df['price'] = df['price'].astype('int')
    #laptops = laptops[(value1 <= laptops['price'] <= value2)]
    #PriceCheck = laptops[laptops['price'].between(value1, value2)]
    #price = st.slider('Price',0,300000,(0,300000))
    nav1, nav2 = st.columns([1,3])

    with nav1:
        selected_search = st.selectbox(
            "Search based on:",
            search_list
        )
    with nav2:
        if selected_search == "Brand and Model":
            laptop_list = PriceCheck['name']
            selected_laptop = st.selectbox(
                "Select a laptop from the search bar.",
                laptop_list
            )

            def recommend(laptop):
                index = laptops[laptops['name'] == laptop].index[0]
                SL = laptops[laptops['name'] == laptop]
                selected_laptop_name = []
                selected_laptop_specs = []
                selected_laptop_description =[]
                selected_laptop_price =[]
                selected_laptop_predicted_price = []
                selected_laptop_url = []

                selected_laptop_name.append(SL['name'].iloc[0])
                selected_laptop_specs.append(SL['specs'].iloc[0])
                selected_laptop_description.append(SL['description'].iloc[0])
                selected_laptop_price.append(SL['price'].iloc[0])
                selected_laptop_predicted_price.append(SL['y_pred'].iloc[0])
                selected_laptop_url.append(SL['laptop-href'].iloc[0])


                distances = sorted(list(enumerate(sig[index])), reverse=True, key=lambda x: x[1])
                recommended_laptop_names = []
                recommended_laptop_specs1 = []
                recommended_laptop_specs = []
                recommended_laptop_description = []
                recommended_laptop_price = []
                recommended_laptop_predicted_price = []
                recommended_laptop_url = []
                for i in distances[1:6]:
                    recommended_laptop_names.append(laptops['name'].iloc[i[0]])
                    recommended_laptop_specs1.append(laptops['specs'].iloc[i[0]])
                    recommended_laptop_specs.append(laptops['cleaned_specs'].iloc[i[0]])
                    recommended_laptop_description.append(laptops['description'].iloc[i[0]])
                    recommended_laptop_price.append(laptops['price'].iloc[i[0]])
                    recommended_laptop_predicted_price.append(laptops['y_pred'].iloc[i[0]])
                    recommended_laptop_url.append(laptops['laptop-href'].iloc[i[0]])
                return  selected_laptop_name,selected_laptop_specs, selected_laptop_description, selected_laptop_price, selected_laptop_predicted_price, selected_laptop_url, recommended_laptop_names, recommended_laptop_specs1, recommended_laptop_specs, recommended_laptop_description, recommended_laptop_price, recommended_laptop_predicted_price, recommended_laptop_url

        elif selected_search == "Specifications":
            laptop_list = PriceCheck['specs'].values
            selected_laptop = st.selectbox(
                "Select a laptop from the search bar.",
                laptop_list
            )

            def recommend(laptop):
                index = laptops[laptops['specs'] == laptop].index[0]
                SL = laptops[laptops['specs'] == laptop]
                selected_laptop_specs = []
                selected_laptop_description = []
                selected_laptop_price = []
                selected_laptop_predicted_price = []
                selected_laptop_url = []
                selected_laptop_name =[]

                selected_laptop_name.append(SL['name'].iloc[0])
                selected_laptop_specs.append(SL['specs'].iloc[0])
                selected_laptop_description.append(SL['description'].iloc[0])
                selected_laptop_price.append(SL['price'].iloc[0])
                selected_laptop_predicted_price.append(SL['y_pred'].iloc[0])
                selected_laptop_url.append(SL['laptop-href'].iloc[0])

                distances = sorted(list(enumerate(sig[index])), reverse=True, key=lambda x: x[1])

                recommended_laptop_names = []
                recommended_laptop_specs1 = []
                recommended_laptop_specs = []
                recommended_laptop_description = []
                recommended_laptop_price = []
                recommended_laptop_predicted_price = []
                recommended_laptop_url = []
                for i in distances[1:6]:
                    recommended_laptop_names.append(laptops['name'].iloc[i[0]])
                    recommended_laptop_specs1.append(laptops['specs'].iloc[i[0]])
                    recommended_laptop_specs.append(laptops['cleaned_specs'].iloc[i[0]])
                    recommended_laptop_description.append(laptops['description'].iloc[i[0]])
                    recommended_laptop_price.append(laptops['price'].iloc[i[0]])
                    recommended_laptop_predicted_price.append(laptops['y_pred'].iloc[i[0]])
                    recommended_laptop_url.append(laptops['laptop-href'].iloc[i[0]])
                return  selected_laptop_name,selected_laptop_specs, selected_laptop_description, selected_laptop_price, selected_laptop_predicted_price, selected_laptop_url, recommended_laptop_names, recommended_laptop_specs1, recommended_laptop_specs, recommended_laptop_description, recommended_laptop_price, recommended_laptop_predicted_price, recommended_laptop_url

    if st.button('Search:'):
        selected_laptop_name,selected_laptop_specs,selected_laptop_description,selected_laptop_price,selected_laptop_predicted_price,selected_laptop_url,recommended_laptop_names, recommended_laptop_specs1, recommended_laptop_specs, recommended_laptop_description, recommended_laptop_price, recommended_laptop_predicted_price, recommended_laptop_url = recommend(selected_laptop)

        st.header('Laptop Selected')
        with st.expander(selected_laptop_name[0], expanded=True):
            st.write('**Specifications**')
            st.text(selected_laptop_specs[0])
            st.write('**Product Description**')
            st.write(selected_laptop_description[0])
            st.write('**Product Link**')
            st.markdown(selected_laptop_url[0])
            st.write('**Price**')
            st.subheader(selected_laptop_price[0])
            st.write('**Recommended Price to buy**')
            st.subheader(selected_laptop_predicted_price[0])
        st.header('Laptops you might like')
        for x in range(5):
            with st.expander(recommended_laptop_names[x], expanded=False):
                st.write('**Specifications**')
                st.text(recommended_laptop_specs1[x])
                st.write('**Product Description**')
                st.write(recommended_laptop_description[x])
                st.write('**Product Link**')
                st.markdown(recommended_laptop_url[x])
                st.write('**Price**')
                st.subheader(recommended_laptop_price[x])
                st.write('**Recommended price to buy:**')
                st.subheader(recommended_laptop_predicted_price[x])



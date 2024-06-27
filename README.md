# Streamlit tutorial - EURO2024 conference programme explorer
## Goal 

- Show-casing the ease of developing interactive web app with `streamlit`
- Introductory and easy-to-follow tutorial material
- Building an interactive conference programme exploring app for the [33rd European Conference on Operational Research (EURO 2024)](https://euro2024cph.dk/)
- Integrating a user-guided operations research model in a web app

Want to check out the resulting web-app? Check out: https://conference-programme-explorer-demo.streamlit.app/

:construction: This README.md is still under construction :construction: 


## Tutorial - topic-wise introduction
:notebook: Want to have a look at how you can build interactive `streamlit` apps step-by-step? 
Browse through the commits of the pull requests linked below :idea:

- [Hello World and basic app development](https://github.com/SanderVA92/conference_programme_explorer/pull/2)
   - Hello World example
   - Collecting user input through widgets like `text_input` and `number_input`
   - Using the input values in other parts of the app
   - Show-case of `streamlit` rerunning the app on each user interaction
   - Ease of using [`session_state`](https://docs.streamlit.io/develop/api-reference/caching-and-state/st.session_state) to share variables between reruns
   - **Structuring the app** using `tabs`, `columns` and `expanders`

- [Interactive programme explorer](https://github.com/SanderVA92/conference_programme_explorer/pull/3)
  - Data loading and basic display using `data_frame`
  - Multiselect, and text-based filters to create **basic filtering functionality**
  - Effectively controlling in the interaction of filters with each other
  - **Making dataframes user-selectable**
  - Dynamic `expander` generation based on select rows
 
- [Integration of optimization models and custom components](https://github.com/SanderVA92/conference_programme_explorer/pull/4)
  - Optimization model creation using `pulp` to **maximize utility of attending conference sessions**
  - Integration of the basic model in a separate tab
  - Functionality to allow **user-guided optimization**
  - [`streamlit-calendar`](https://github.com/im-perativa/streamlit-calendar) integration


## To-do / will come soonish

- [ ] Add slides from tutorial presentation

# EURO2024 conference programme explorer
_Material initially developed as part of a `streamlit` tutorial at the [EURO conference in Copenhagen](https://euro2024cph.dk/)_

- Check the final result here: [![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)]([https://calendar-component.streamlit.app/](https://tinyurl.com/EURO2024-streamlit))
- Original presentation can be found [here](https://github.com/SanderVA92/conference_programme_explorer/blob/sidebar_view/docs/MAI%20at%20EURO%202024%20-%20Streamlit.pdf)
- Feedback, or want to get in touch? [![Linkedin](https://i.sstatic.net/gVE0j.png) LinkedIn](https://www.linkedin.com/in/sander-van-aken/)

## Goal of this repo

- Show-casing the **ease of developing interactive web apps** with `streamlit`
- Introductory and easy-to-follow tutorial material (see section below)
- Building an interactive conference programme exploring app for the [33rd European Conference on Operational Research (EURO 2024)](https://euro2024cph.dk/)
- Integrating a user-guided operations research model in a web app

## Running the app locally

<details>
  <summary>Click for instructions</summary>
  

### 1. Setup
First, clone the repository:

```
git clone https://github.com/conference_programme_explorer.git
cd conference_programme_explorer
```

### 2. Install the required dependencies
For this project, `poetry` is used as a package manager. More information, including installation instructions - on the [project's website](https://python-poetry.org/docs/)

```
poetry install
```

### 3. Running the app
To run your app locally, you can launch it from the terminal.
```
streamlit run streamlitapp/programme_explorer.py
```

Want to show the optimization tab and play around with it? You can manage this by means of a feature toggle stored. For that, create a `.streamlit/secrets.toml` file and add the following content:

```
[feature_toggles]
show_optimization_tab = 'False'
```

</details>

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

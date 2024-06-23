import streamlit as st
import data.load as data_loader
from config import AppConfig

st.set_page_config(layout="wide")


def main() -> None:
    filepath_programme = AppConfig.FILEPATH_CONFERENCE_PROGRAMME
    df_complete_programme = data_loader.load_and_prepare_programme_data(filepath_programme)

    st.dataframe(
        df_complete_programme,
        column_order=['Schedule', 'Track Code', 'Session Name', 'Title', 'Keywords'],
        hide_index=True
    )


if __name__ == '__main__':
    st.title('EURO2024 Conference Programme Explorer')

    st.info(
        f'''
            Hi there, this streamlit application allows you to explore the EURO2024 conference programme. The data 
            shown here originates from an export created on {AppConfig.DATE_OF_PROGRAMME_EXPORT}. For the most 
            up-to-date programme, please visit {AppConfig.CONFERENCE_PROGRAMME_LINK}.
        '''
    )

    main()

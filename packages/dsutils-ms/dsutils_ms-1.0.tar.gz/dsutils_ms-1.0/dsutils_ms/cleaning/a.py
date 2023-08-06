# trim_spaces

# dropduplicates

# unidecode

# rename columns (give possibility to rename columns through a dictionary)
# gs_dataframe.columns = list(map(lambda x: inflection.underscore(x).strip().replace('-', '').replace('/', '').replace(
#                 '\\', '').replace('?', '').replace('!', '').replace(',', '').replace('.', ''), gs_dataframe.columns))


#         try:
#             if dropna is True:
#                 gs_dataframe = (
#                     gs_dataframe.replace("", np.nan, regex=True)
#                     .dropna(how="all")
#                     .reset_index(drop=True)
#                 )
#         except Exception as exc:
#             raise Exception("Removing missing values error") from exc

#         try:
#             if trim_spaces is True:
#                 gs_dataframe = gs_dataframe.apply(
#                     lambda x: x.apply(str).str.strip().str.replace("  ", " ")
#                     if x.dtype == "object"
#                     else x
#                 )
#         except Exception as exc:
#             raise Exception("Trim whitespaces error") from exc



        # try:
        #     HEADER_ROW = 0
        #     VALUES_ROWS = 1
        #     gs_dataframe = pd.DataFrame(
        #         gs_data[VALUES_ROWS:], columns=gs_data[HEADER_ROW]
        #     )

        #     gs_dataframe.columns = (
        #         gs_dataframe.columns.str.strip()
        #         .str.lower()
        #         .str.replace(" ", "_")
        #     )
        #     gs_dataframe.columns = list(map(unidecode, gs_dataframe.columns))

        #     gs_dataframe.columns = list(map(lambda x: inflection.underscore(x).strip().replace('-', '').replace('/', '').replace(
        #         '\\', '').replace('?', '').replace('!', '').replace(',', '').replace('.', ''), gs_dataframe.columns))

        # except Exception as exc:
        #     raise Exception("Cell Lookup Error") from exc
        
        # try:
        #     if subset is not None:
        #         gs_dataframe = gs_dataframe[subset].copy()
        # except Exception as exc:
        #     raise Exception("Subset Selection Error") from exc
        
        # try:
        #     if dropna is True:
        #         gs_dataframe = (
        #             gs_dataframe.replace("", np.nan, regex=True)
        #             .dropna(how="all")
        #             .reset_index(drop=True)
        #         )
        # except Exception as exc:
        #     raise Exception("Removing missing values error") from exc
        
        
        # try:
        #     if trim_spaces is True:
        #         gs_dataframe = gs_dataframe.apply(
        #             lambda x: x.apply(str).str.strip().str.replace("  ", " ")
        #             if x.dtype == "object"
        #             else x
        #         )
        # except Exception as exc:
        #     raise Exception("Trim whitespaces error") from exc
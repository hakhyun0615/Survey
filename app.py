import streamlit as st
import pandas as pd
import plotly.express as px

#
st.sidebar.title('설문조사 분석')

def load_data(age_option, gender_option, app_option):
    df = pd.read_excel('맛집 앱 및 배달 앱에 관한 설문(응답).xlsx')
    df.drop(['타임스탬프','추첨을 통해 스타벅스 기프티콘을 드립니다!\n전화번호를 적어주세요! \n(본 내용은 추첨 이후 즉시 폐기 예정입니다)'], axis=1, inplace=True)
    if (age_option != '전체'):
        df = df[df['1. 귀하의 연령대는 어떻게 되시나요?'] == age_option]
    if (gender_option != '전체'):
        df = df[df['2. 귀하의 성별은 무엇인가요?'] == gender_option]
    if (app_option != '전체'):
        df = df[df['4. 식당을 찾을 때 어떤 앱을 사용하나요? 사용하시는 앱을 모두 골라주세요!'].str.contains(app_option)]
    return df
def transform_importance(df):
    cols = [
        '3. 음식점 및 카페를 찾을 때 어떤 정보별로 중요도를 골라주세요! [가격]',
        '3. 음식점 및 카페를 찾을 때 어떤 정보별로 중요도를 골라주세요! [메뉴]',
        '3. 음식점 및 카페를 찾을 때 어떤 정보별로 중요도를 골라주세요! [영업시간]',
        '3. 음식점 및 카페를 찾을 때 어떤 정보별로 중요도를 골라주세요! [음식점 전화번호]',
        '3. 음식점 및 카페를 찾을 때 어떤 정보별로 중요도를 골라주세요! [매장 분위기]',
        '3. 음식점 및 카페를 찾을 때 어떤 정보별로 중요도를 골라주세요! [매장 서비스(ex, 24시간, 주차가능, 애완동물반입가능)]'
    ]
    for col in cols:
        df[col] = df[col].str.replace('매우 중요하지 않음','1')
        df[col] = df[col].str.replace('중요하지 않음','2')
        df[col] = df[col].str.replace('보통','3')
        df[col] = df[col].str.replace('매우 중요','5')
        df[col] = df[col].str.replace('중요','4')
        df[col] = df[col].astype('int')

    return df
def importance_star_chart(df):
    df = transform_importance(df)

    price = df['3. 음식점 및 카페를 찾을 때 어떤 정보별로 중요도를 골라주세요! [가격]'].mean()
    menu = df['3. 음식점 및 카페를 찾을 때 어떤 정보별로 중요도를 골라주세요! [메뉴]'].mean()
    time = df['3. 음식점 및 카페를 찾을 때 어떤 정보별로 중요도를 골라주세요! [영업시간]'].mean()
    phone = df['3. 음식점 및 카페를 찾을 때 어떤 정보별로 중요도를 골라주세요! [음식점 전화번호]'].mean()
    atmosphere = df['3. 음식점 및 카페를 찾을 때 어떤 정보별로 중요도를 골라주세요! [매장 분위기]'].mean()
    service = df['3. 음식점 및 카페를 찾을 때 어떤 정보별로 중요도를 골라주세요! [매장 서비스(ex, 24시간, 주차가능, 애완동물반입가능)]'].mean()

    plot_df = pd.DataFrame(
        dict(
            r = [price, menu, time, phone, atmosphere, service],
            theta = ['가격','메뉴','영업시간','음식점 전화번호', '매장 분위기', '매장 서비스']
        )
    )
    fig = px.line_polar(plot_df, r='r', theta='theta', line_close=True)
    st.plotly_chart(fig)
def else_star_chart(df, what):
    if (what == '사용 앱'):
        dic = {'네이버 검색':0,'네이버 지도':0,'카카오맵':0,'인스타그램 검색':0,'유튜브':0,'망고플레이트':0,'다이닝코드':0,'식신':0}
        for i in range(len(df)):
            for k in dic:
                try:
                    if (k in df['4. 식당을 찾을 때 어떤 앱을 사용하나요? 사용하시는 앱을 모두 골라주세요!'].iloc[i]):
                        dic[k] += 1
                except:
                    pass
        plot_df = pd.DataFrame(
            dict(
                r = [dic[k] for k in dic],
                theta = [k for k in dic]
            )
        )
        fig = px.line_polar(plot_df, r='r', theta='theta', line_close=True)
        st.plotly_chart(fig)
    elif (what == '사용 앱 사용 이유'):
        dic = {'UI/UX가 편해서':0,'음식점 정보가 많아서':0,'친구&지인이 같이 쓰자고 해서':0,'처음 사용한 뒤 익숙해져서':0,'이벤트가 많아서':0,'앱의 속도가 빨라서':0,'원하는 정보를 얻을 수 있어서':0}
        for i in range(len(df)):
            for k in dic:
                try:
                    if (k in df['1. 해당 앱들을 사용하시는 이유는 무엇인가요?'].iloc[i]):
                        dic[k] += 1
                except:
                    pass
        plot_df = pd.DataFrame(
            dict(
                r = [dic[k] for k in dic],
                theta = [k for k in dic]
            )
        )
        fig = px.line_polar(plot_df, r='r', theta='theta', line_close=True)
        st.plotly_chart(fig)
    elif (what == '사용 앱 불편 이유'):
        dic = {'UI/UX가 불편함':0,'회원가입 절차가 번거롭다':0,'음식점 정보가 적음':0,'음식점 공유할 때 타 메신저를 이용해야하는 불편함':0,'앱의 속도가 느림':0,'이벤트가 적다':0,'원하는 정보가 부족하다':0}
        for i in range(len(df)):
            for k in dic:
                try:
                    if (k in df["해당 앱들에서 불편했던 점이 있을까요?\n보기 외에 더 있으시면 '기타'란에 추가로 작성해주세요.\n(없으면 기타에 '없음')"].iloc[i]):
                        dic[k] += 1
                except:
                    pass
        plot_df = pd.DataFrame(
            dict(
                r = [dic[k] for k in dic],
                theta = [k for k in dic]
            )
        )
        fig = px.line_polar(plot_df, r='r', theta='theta', line_close=True)
        st.plotly_chart(fig)
    elif (what == '우리 앱 기능 선호도'):
        dic = {'지인들과 지도에서 원하는 음식점 위치를 실시간 공유하는 기능':0,'지도 상에서 음식점의 세부정보(대표메뉴, 평점 등)를 직관적으로 확인 가능한 점':0,'음식점의 리뷰를 매장분위기, 메뉴별 리뷰로 따로 작성 및 열람 가능한 기능':0,'여러 배달 음식점 간의 배달음식점의 배달비 비교 기능':0}
        for i in range(len(df)):
            for k in dic:
                try:
                    if (k in df["맛집 검색 앱에 있다면 좋을 것 같은 기능을 골라주세요!\n보기 외에 더 있으시면 '기타'란에 추가로 작성해주세요."].iloc[i]):
                        dic[k] += 1
                except:
                    pass
        plot_df = pd.DataFrame(
            dict(
                r = [dic[k] for k in dic],
                theta = [k for k in dic]
            )
        )
        fig = px.line_polar(plot_df, r='r', theta='theta', line_close=True)
        st.plotly_chart(fig)
def importance_bar_chart(df):
    df = transform_importance(df)

    price = df['3. 음식점 및 카페를 찾을 때 어떤 정보별로 중요도를 골라주세요! [가격]'].mean()
    menu = df['3. 음식점 및 카페를 찾을 때 어떤 정보별로 중요도를 골라주세요! [메뉴]'].mean()
    time = df['3. 음식점 및 카페를 찾을 때 어떤 정보별로 중요도를 골라주세요! [영업시간]'].mean()
    phone = df['3. 음식점 및 카페를 찾을 때 어떤 정보별로 중요도를 골라주세요! [음식점 전화번호]'].mean()
    atmosphere = df['3. 음식점 및 카페를 찾을 때 어떤 정보별로 중요도를 골라주세요! [매장 분위기]'].mean()
    service = df['3. 음식점 및 카페를 찾을 때 어떤 정보별로 중요도를 골라주세요! [매장 서비스(ex, 24시간, 주차가능, 애완동물반입가능)]'].mean()

    fig = px.bar(x = [price, menu, time, phone, atmosphere, service], y = ['가격','메뉴','영업시간','음식점 전화번호', '매장 분위기', '매장 서비스'])
    st.plotly_chart(fig)
def else_bar_chart(df, what):
    if (what == '사용 앱'):
        dic = {'네이버 검색':0,'네이버 지도':0,'카카오맵':0,'인스타그램 검색':0,'유튜브':0,'망고플레이트':0,'다이닝코드':0,'식신':0}
        for i in range(len(df)):
            for k in dic:
                try:
                    if (k in df['4. 식당을 찾을 때 어떤 앱을 사용하나요? 사용하시는 앱을 모두 골라주세요!'].iloc[i]):
                        dic[k] += 1
                except:
                    pass
        plot_df = pd.DataFrame(
            dict(
                r = [dic[k] for k in dic],
                theta = [k for k in dic]
            )
        )
        fig = px.bar(plot_df, x = 'theta', y = 'r')
        st.plotly_chart(fig)
    elif (what == '사용 앱 사용 이유'):
        dic = {'UI/UX가 편해서':0,'음식점 정보가 많아서':0,'친구&지인이 같이 쓰자고 해서':0,'처음 사용한 뒤 익숙해져서':0,'이벤트가 많아서':0,'앱의 속도가 빨라서':0,'원하는 정보를 얻을 수 있어서':0}
        for i in range(len(df)):
            for k in dic:
                try:
                    if (k in df['1. 해당 앱들을 사용하시는 이유는 무엇인가요?'].iloc[i]):
                        dic[k] += 1
                except:
                    pass
        plot_df = pd.DataFrame(
            dict(
                r = [dic[k] for k in dic],
                theta = [k for k in dic]
            )
        )
        fig = px.bar(plot_df, x = 'theta', y = 'r')
        st.plotly_chart(fig)
    elif (what == '사용 앱 불편 이유'):
        dic = {'UI/UX가 불편함':0,'회원가입 절차가 번거롭다':0,'음식점 정보가 적음':0,'음식점 공유할 때 타 메신저를 이용해야하는 불편함':0,'앱의 속도가 느림':0,'이벤트가 적다':0,'원하는 정보가 부족하다':0}
        for i in range(len(df)):
            for k in dic:
                try:
                    if (k in df["해당 앱들에서 불편했던 점이 있을까요?\n보기 외에 더 있으시면 '기타'란에 추가로 작성해주세요.\n(없으면 기타에 '없음')"].iloc[i]):
                        dic[k] += 1
                except:
                    pass
        plot_df = pd.DataFrame(
            dict(
                r = [dic[k] for k in dic],
                theta = [k for k in dic]
            )
        )
        fig = px.bar(plot_df, x = 'theta', y = 'r')
        st.plotly_chart(fig)
    elif (what == '우리 앱 기능 선호도'):
        dic = {'지인들과 지도에서 원하는 음식점 위치를 실시간 공유하는 기능':0,'지도 상에서 음식점의 세부정보(대표메뉴, 평점 등)를 직관적으로 확인 가능한 점':0,'음식점의 리뷰를 매장분위기, 메뉴별 리뷰로 따로 작성 및 열람 가능한 기능':0,'여러 배달 음식점 간의 배달음식점의 배달비 비교 기능':0}
        for i in range(len(df)):
            for k in dic:
                try:
                    if (k in df["맛집 검색 앱에 있다면 좋을 것 같은 기능을 골라주세요!\n보기 외에 더 있으시면 '기타'란에 추가로 작성해주세요."].iloc[i]):
                        dic[k] += 1
                except:
                    pass
        plot_df = pd.DataFrame(
            dict(
                r = [dic[k] for k in dic],
                theta = [k for k in dic]
            )
        )
        fig = px.bar(plot_df, x = 'theta', y = 'r')
        st.plotly_chart(fig)

#
age_option = st.sidebar.selectbox('연령을 선택해주세요.',pd.Series(['전체','10대','20~24세','25~29세','30대','40대','50대','60대 이상']))
gender_option = st.sidebar.selectbox('성별을 선택해주세요.',pd.Series(['전체','남자','여자']))
app_option = st.sidebar.selectbox('사용 앱을 선택해주세요.',pd.Series(['전체','네이버 검색','네이버 지도','카카오맵','인스타그램 검색','유튜브','망고플레이트','다이닝코드','식신']))

#
see_option = st.sidebar.selectbox('보고 싶은 형식을 선택해주세요.',pd.Series(['표','스타차트','막대차트']))

#
if (see_option == '표'):
    df = load_data(age_option, gender_option, app_option)
    st.dataframe(df)
elif (see_option == '스타차트'):
    df = load_data(age_option, gender_option, app_option)
    st.subheader('중요도')
    importance_star_chart(df)
    st.subheader('사용 앱')
    else_star_chart(df, '사용 앱')
    st.subheader('사용 앱 사용 이유')
    else_star_chart(df, '사용 앱 사용 이유')
    st.subheader('사용 앱 불편 이유')
    else_star_chart(df, '사용 앱 불편 이유')
    st.subheader('우리 앱 기능 선호도')
    else_star_chart(df, '우리 앱 기능 선호도')
elif (see_option == '막대차트'):
    df = load_data(age_option, gender_option, app_option)
    st.subheader('중요도')
    importance_bar_chart(df)
    st.subheader('사용 앱')
    else_bar_chart(df, '사용 앱')
    st.subheader('사용 앱 사용 이유')
    else_bar_chart(df, '사용 앱 사용 이유')
    st.subheader('사용 앱 불편 이유')
    else_bar_chart(df, '사용 앱 불편 이유')
    st.subheader('우리 앱 기능 선호도')
    else_bar_chart(df, '우리 앱 기능 선호도')
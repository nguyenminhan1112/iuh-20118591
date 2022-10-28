from http import server
from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd
import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate('./iuh-20085541-de3e6-firebase-adminsdk-jq7sn-3b286dd872.json')
appLoadData = firebase_admin.initialize_app(cred)

dbFireStore = firestore.client()

queryResults = list(dbFireStore.collection(u'tbl-20085541').stream())
listQueryResult = list(map(lambda x: x.to_dict(), queryResults))

df = pd.DataFrame(listQueryResult)

df["YEAR_ID"] = df["YEAR_ID"].astype("str")
df["QTR_ID"] = df["QTR_ID"].astype("str")
df["PROFIT"]=df["SALES"]-(df["QUANTITYORDERED"]*df["PRICEEACH"])

app = Dash(__name__)
server=app.server

app.title = "Danh Mục Sản Phẩm Tiềm Năng"

#tổng doanh số
sales = sum(df["SALES"])

#tổng lợi nhuận
profit = sum(df['PROFIT'])

#top doanh số
topSales = df.groupby(['CATEGORY']).sum('SALES').max().SALES
maSP_TopSales = df.groupby(['CATEGORY']).sum('SALES').sort_values(by="SALES", ascending=False).reset_index().head(1)['CATEGORY'][0]

#top lợi nhuận
topProfit = df.groupby(['CATEGORY']).sum('PROFIT').max().PROFIT
maSP_TopProfit = df.groupby(['CATEGORY']).sum('PROFIT').sort_values(by="PROFIT", ascending=False).reset_index().head(1)['CATEGORY'][0]

#bar chart doanh số từng năm
data=df.groupby(['YEAR_ID'])['SALES'].sum().reset_index(name='SALES')
data1=df.groupby(["YEAR_ID"])["PROFIT"].sum().reset_index(name="PROFIT")
data=data.merge(data1)
figDoanhSoBanHang = px.bar(data, x="YEAR_ID", y="SALES", 
barmode="group", color="YEAR_ID", title='Doanh số bán hàng theo năm',
labels={'YEAR_ID':"Năm", 'Sum':'Doanh số bán hàng'})

#line chart lợi nhuận từng năm

figLoiNhuanBanHang=px.line(data,x="YEAR_ID",y="PROFIT", title='Lợi nhuận bán hàng theo năm',
labels={'YEAR_ID':'Năm', 'Sum':'Lợi nhuận bán hàng'})

#sunburst tỉ lệ doanh số theo danh mục và năm
data2=df.groupby(['YEAR_ID','CATEGORY'])['SALES'].sum().reset_index(name='SALES')
figTyLeDoanhSo= px.sunburst(data2, path=[ 'YEAR_ID','CATEGORY'], values='SALES',
color='SALES',
labels={'parent':'Năm','label':'danh mục','SALES':'Doanh số bán hàng'},
title='Tỉ lệ đóng góp của doanh số theo từng danh mục trong từng năm')

#sunburst tỉ lệ lợi nhuận theo danh mục và năm
data2["YEAR_ID"] = data2["YEAR_ID"].astype("str")
data2["CATEGORY"]=data2["CATEGORY"].astype("str")
data["YEAR_ID"] = data["YEAR_ID"].astype("str")
data3=df.groupby(['YEAR_ID','CATEGORY'])['PROFIT'].sum().reset_index(name='PROFIT')
data3["YEAR_ID"] = data3["YEAR_ID"].astype("str")
data3["CATEGORY"]=data3["CATEGORY"].astype("str")
figTyLeLoiNhuan= px.sunburst(data3, path=[ 'YEAR_ID','CATEGORY'], values='PROFIT',
color='PROFIT',
labels={'parent':'Năm','label':'danh mục','PROFIT':'Lợi nhuận'},
title='Tỉ lệ đóng góp của lợi nhuận theo từng danh mục trong từng năm')
app.layout = html.Div(
    children=[
        html.Div(
            children=[
                html.H3(
                    "Trường: IUH, Lớp: DHHTTT16C Nguyen Thi Ngoc Hien-20118591", className="header-title"
                    "XÂY DỰNG SẢN PHẨM DANH MỤC TIỀM NĂNG "
                ),
                
            ],
            className="header",
        ),
        html.Div(
            children=[
                html.Div(
                children=html.Div(
                    children=[
                        html.H4(
                            "$", 
                        ),
                        "{:.2f}"+"$"
                    ],
                    className="label"
                    ),className="card c1"
                ),
                html.Div(
                children=html.Div(
                    children=[
                        html.H4(
                            "$", 
                        ),
                        "{:.2f}".format(profit)
                    ],
                    className="label"
                    ),className="card c1"
                ),
                html.Div(
                children=html.Div(
                    children=[
                        html.H4(
                            "$
                        ),
                        maSP_TopSales+', '+"{:.2f}".format(topSales)
                    ],
                    className="label"
                    ),className="card c1"
                ),
                html.Div(
                children=html.Div(
                    children=[
                        html.H4(
                            "$", 
                        ),
                        maSP_TopProfit+', '+"{:.2f}".format(topProfit)
                    ],
                    className="label" 
                    ),className="card c1"
                ),
                html.Div(
                children=dcc.Graph(
                    figure=figDoanhSoBanHang,
                    className="hist"
                    ),className="card c2"
                ),
                html.Div(
                children=dcc.Graph(
                    figure=figTyLeDoanhSo,
                    className="hist"
                    ),className="card c2"
                ),
                html.Div(
                children=dcc.Graph(
                    figure=figLoiNhuanBanHang,
                    className="hist"
                    ),className="card c2"
                ),
                html.Div(
                children=dcc.Graph(
                    figure=figTyLeLoiNhuan,
                    className="hist"
                    ),className="card c2"
                )
            ],className="wrapper"
        )
    ])

if __name__ == '__main__':
    app.run_server(debug=True, port=8070)

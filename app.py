import streamlit as st
import yfinance as yf
import pandas as pd

st.title("📊 Personal Portfolio Tracker")

# 1. Nhập danh mục đầu tư
st.sidebar.header("Nhập danh mục")
ticker = st.sidebar.text_input("Mã chứng khoán (VD: AAPL, VCB.VN):", "AAPL")
shares = st.sidebar.number_input("Số lượng:", min_value=0.1, value=10.0)

if st.sidebar.button("Thêm vào danh mục"):
    # Giả lập lưu vào session state
    if 'portfolio' not in st.session_state:
        st.session_state.portfolio = pd.DataFrame(columns=['Ticker', 'Shares'])
    
    new_row = pd.DataFrame({'Ticker': [ticker], 'Shares': [shares]})
    st.session_state.portfolio = pd.concat([st.session_state.portfolio, new_row], ignore_index=True)

# 2. Hiển thị bảng danh mục
if 'portfolio' in st.session_state:
    st.write("### Danh mục hiện tại:")
    df = st.session_state.portfolio
    
    # Lấy giá thị trường thực tế
    # Thay đoạn cũ bằng đoạn này để kiểm tra lỗi
    prices = []
    for t in df['Ticker']:
        ticker_data = yf.Ticker(t)
        hist = ticker_data.history(period='1d')
        
        if not hist.empty:
            price = hist['Close'].iloc[-1]
            prices.append(price)
        else:
            st.warning(f"Không tìm thấy dữ liệu cho mã: {t}. Vui lòng kiểm tra lại (ví dụ: thêm .VN)")
            prices.append(0.0) # Gán giá bằng 0 nếu lỗi

# Filmlist

Website được xây dựng để những khán giả điện ảnh có thể tra cứu, lưu lại và theo dõi chi tiết, thông tin về các bộ phim.

## Mô tả

Website được xây dựng bằng Flask, CSS, HTML và JavaScript. Trang web giúp người dùng theo dõi những bộ phim đang nổi, những bộ phim đang được phát hành, những bộ phim kinh điển được đánh giá cao, cũng như là các phim sắp được cho ra mắt. Người dùng có thể xem thông tin, mô tả của từng bộ phim, lưu vào các danh sách cá nhân, từ cơ sở dữ liệu hơn 300,000 phim. Người dùng có thể nâng cấp hạng của tài khoản để có thêm tính năng tải các poster hay backdrop của phim, cũng như theo dõi các video clip được cắt từ phim. Website có hỗ trợ đa ngôn ngữ. 
* Trang chủ trình bày những bộ phim ở mỗi hạng mục, người dùng có thể browse phim từ đây.
* Nếu muốn xem nhiều phim hơn ở mỗi hạng mục, người dùng có thể truy cập từ navbar mỗi trang hạng mục cụ thể.
* Mỗi phim có một trang riêng, trình bày thông tin về phim. Người dùng ấn vào poster phim ở bất kỳ trang nào của web để truy cập trang riêng của phim.
* Mục profile cho người dùng xem thông tin của tài khoản.
* Trang search cho phép người dùng tìm phim theo tên.
* Trang list cho phép người dùng tạo và xem các danh sách phim của tài khoản. Người dùng có thể thoải mái tạo và đặt tên riêng cho mỗi danh sách để có thể tiện theo dõi.
* Người dùng có thể đổi ngôn ngữ với công cụ translate ở cuối trang.

## Sử dụng

### Dependencies

* Flask  
* Flask session để quản lý phiên truy cập người dùng
* Flask caching cho việc cache lại các API call
* cs50 để truy cập cơ sở dữ liệu SQLite
* werkzeug để xử lý xác thực người dùng
* luhnchecker xử lý phần thanh toán tín dụng
* Cài đặt:
```
pip install -r requirements.txt
```

### Cài đặt

* Clone repository https://github.com/bachdd22/movie-recommendation-system
* Cài đặt các dependencies.

### Executing program

* Dùng câu lệnh Flask để chạy chương trình:
```
flask run
```


## Bài tập lớn CNPM 5/2024


* Đinh Duy Bách - 22022531
* Lê Hữu Đức - 22022535
* Báo cáo và video demo: https://wide-glazer-4f5.notion.site/B-o-c-o-b-i-t-p-l-n-CNPM-e6920c056c224b768efb5d51c74459e2?pvs=4
  


## License

[MIT](LICENSE)

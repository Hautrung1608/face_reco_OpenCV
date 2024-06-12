import matplotlib.pyplot as plt
import matplotlib.image as mpimg

def hien_thi_anh(id):
    ten_anh = f"show/image_{id}.png"  # Tạo tên tệp ảnh dựa trên ID
    img = mpimg.imread(ten_anh)
    plt.imshow(img)
    plt.axis('off')  # Tắt trục
    plt.show()

# Sử dụng hàm để hiển thị ảnh dựa trên ID
# Thay đổi ID tại đây để hiển thị ảnh khác
id = 7  

hien_thi_anh(id)

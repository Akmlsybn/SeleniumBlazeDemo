import pytest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

@pytest.fixture
def driver():
    options = webdriver.ChromeOptions()
    options.add_experimental_option("detach", True)
    driver = webdriver.Chrome(options=options)
    driver.maximize_window()
    driver.implicitly_wait(10)
    yield driver
    driver.quit()

# --- FUNGSI BANTUAN (HELPERS) ---
def go_to_purchase(driver):
    driver.get("https://blazedemo.com/")
    driver.find_element(By.CSS_SELECTOR, "input[value='Find Flights']").click()
    time.sleep(1) # Tunggu loading halaman reserve
    driver.find_elements(By.CSS_SELECTOR, "input[value='Choose This Flight']")[0].click()
    time.sleep(1) # Tunggu loading halaman purchase

def submit_purchase(driver):
    driver.find_element(By.CSS_SELECTOR, "input[value='Purchase Flight']").click()
    time.sleep(2) # Tunggu proses pembayaran selesai agar tidak terlalu cepat

# ==========================================
# SKN-01: Pemilihan Rute Penerbangan
# ==========================================
def test_skn_01_positif_rute_berbeda(driver):
    driver.get("https://blazedemo.com/")
    Select(driver.find_element(By.NAME, "fromPort")).select_by_value("Paris")
    Select(driver.find_element(By.NAME, "toPort")).select_by_value("London")
    driver.find_element(By.CSS_SELECTOR, "input[value='Find Flights']").click()
    time.sleep(1)
    assert "Flights from Paris to London" in driver.find_element(By.TAG_NAME, "h3").text

def test_skn_01_negatif_tanpa_ubah_rute(driver):
    driver.get("https://blazedemo.com/")
    driver.find_element(By.CSS_SELECTOR, "input[value='Find Flights']").click()
    time.sleep(1)
    assert "Flights from Paris to Buenos Aires" in driver.find_element(By.TAG_NAME, "h3").text

# ==========================================
# SKN-02: Akses Halaman Pemesanan
# ==========================================
def test_skn_02_positif_akses_pemesanan(driver):
    go_to_purchase(driver)
    assert "purchase.php" in driver.current_url

def test_skn_02_negatif_akses_direct_tanpa_rute(driver):
    driver.get("https://blazedemo.com/reserve.php")
    table_rows = driver.find_elements(By.TAG_NAME, "tr")
    assert len(table_rows) > 1

# ==========================================
# SKN-03: Input Nama Penumpang
# ==========================================
def test_skn_03_positif_input_nama(driver):
    go_to_purchase(driver)
    driver.find_element(By.ID, "inputName").send_keys("Amay")
    submit_purchase(driver)
    assert "Thank you" in driver.page_source

def test_skn_03_negatif_kosongkan_nama(driver):
    go_to_purchase(driver)
    driver.find_element(By.ID, "inputName").clear()
    submit_purchase(driver)
    assert "confirmation.php" in driver.current_url

# ==========================================
# SKN-04: Input Alamat
# ==========================================
def test_skn_04_positif_input_alamat(driver):
    go_to_purchase(driver)
    driver.find_element(By.ID, "address").send_keys("Jl. Brigjen Hasan Basri")
    submit_purchase(driver)
    assert "Thank you" in driver.page_source

def test_skn_04_negatif_kosongkan_alamat(driver):
    go_to_purchase(driver)
    driver.find_element(By.ID, "address").clear()
    submit_purchase(driver)
    assert "confirmation.php" in driver.current_url

# ==========================================
# SKN-05: Input Kota (City)
# ==========================================
def test_skn_05_positif_input_kota(driver):
    go_to_purchase(driver)
    driver.find_element(By.ID, "city").send_keys("Banjarmasin")
    submit_purchase(driver)
    assert "Thank you" in driver.page_source

def test_skn_05_negatif_kosongkan_kota(driver):
    go_to_purchase(driver)
    driver.find_element(By.ID, "city").clear()
    submit_purchase(driver)
    assert "confirmation.php" in driver.current_url

# ==========================================
# SKN-06: Input Provinsi (State)
# ==========================================
def test_skn_06_positif_input_state(driver):
    go_to_purchase(driver)
    driver.find_element(By.ID, "state").send_keys("Kalimantan Selatan")
    submit_purchase(driver)
    assert "Thank you" in driver.page_source

def test_skn_06_negatif_kosongkan_state(driver):
    go_to_purchase(driver)
    driver.find_element(By.ID, "state").clear()
    submit_purchase(driver)
    assert "confirmation.php" in driver.current_url

# ==========================================
# SKN-07: Kehadiran Data Kode Pos (Zip Code)
# ==========================================
def test_skn_07_positif_input_zip(driver):
    go_to_purchase(driver)
    driver.find_element(By.ID, "zipCode").send_keys("70123")
    submit_purchase(driver)
    assert "Thank you" in driver.page_source

def test_skn_07_negatif_kosongkan_zip(driver):
    go_to_purchase(driver)
    driver.find_element(By.ID, "zipCode").clear()
    submit_purchase(driver)
    assert "confirmation.php" in driver.current_url

# ==========================================
# SKN-08: Validasi Format Kode Pos
# ==========================================
def test_skn_08_positif_format_zip_angka(driver):
    go_to_purchase(driver)
    driver.find_element(By.ID, "zipCode").send_keys("12345")
    submit_purchase(driver)
    assert "Thank you" in driver.page_source

def test_skn_08_negatif_format_zip_huruf(driver):
    go_to_purchase(driver)
    driver.find_element(By.ID, "zipCode").send_keys("ABCDE")
    submit_purchase(driver)
    assert "confirmation.php" in driver.current_url

# ==========================================
# SKN-09: Pemilihan Tipe Kartu Kredit
# ==========================================
def test_skn_09_positif_pilih_visa(driver):
    go_to_purchase(driver)
    Select(driver.find_element(By.ID, "cardType")).select_by_value("visa")
    submit_purchase(driver)
    assert "Thank you" in driver.page_source

def test_skn_09_negatif_pilih_amex(driver):
    go_to_purchase(driver)
    Select(driver.find_element(By.ID, "cardType")).select_by_value("amex")
    submit_purchase(driver)
    assert "confirmation.php" in driver.current_url

# ==========================================
# SKN-10: Kehadiran Nomor Kartu Kredit
# ==========================================
def test_skn_10_positif_input_cc(driver):
    go_to_purchase(driver)
    driver.find_element(By.ID, "creditCardNumber").send_keys("1234567890123456")
    submit_purchase(driver)
    assert "Thank you" in driver.page_source

def test_skn_10_negatif_kosongkan_cc(driver):
    go_to_purchase(driver)
    driver.find_element(By.ID, "creditCardNumber").clear()
    submit_purchase(driver)
    assert "confirmation.php" in driver.current_url

# ==========================================
# SKN-11: Validasi Format Nomor Kartu
# ==========================================
def test_skn_11_positif_format_cc_angka(driver):
    go_to_purchase(driver)
    driver.find_element(By.ID, "creditCardNumber").send_keys("1111222233334444")
    submit_purchase(driver)
    assert "Thank you" in driver.page_source

def test_skn_11_negatif_format_cc_huruf(driver):
    go_to_purchase(driver)
    driver.find_element(By.ID, "creditCardNumber").send_keys("KARTUKU")
    submit_purchase(driver)
    assert "confirmation.php" in driver.current_url

# ==========================================
# SKN-12: Validasi Panjang Nomor Kartu
# ==========================================
def test_skn_12_positif_panjang_cc_valid(driver):
    go_to_purchase(driver)
    driver.find_element(By.ID, "creditCardNumber").send_keys("1234567890123456")
    submit_purchase(driver)
    assert "Thank you" in driver.page_source

def test_skn_12_negatif_panjang_cc_pendek(driver):
    go_to_purchase(driver)
    driver.find_element(By.ID, "creditCardNumber").send_keys("123")
    submit_purchase(driver)
    assert "confirmation.php" in driver.current_url

# ==========================================
# SKN-13: Kehadiran Bulan Kedaluwarsa
# ==========================================
def test_skn_13_positif_input_bulan(driver):
    go_to_purchase(driver)
    driver.find_element(By.ID, "creditCardMonth").clear()
    driver.find_element(By.ID, "creditCardMonth").send_keys("11")
    submit_purchase(driver)
    assert "Thank you" in driver.page_source

def test_skn_13_negatif_kosongkan_bulan(driver):
    go_to_purchase(driver)
    driver.find_element(By.ID, "creditCardMonth").clear()
    submit_purchase(driver)
    assert "confirmation.php" in driver.current_url

# ==========================================
# SKN-14: Validasi Logika Bulan
# ==========================================
def test_skn_14_positif_logika_bulan_valid(driver):
    go_to_purchase(driver)
    driver.find_element(By.ID, "creditCardMonth").clear()
    driver.find_element(By.ID, "creditCardMonth").send_keys("12")
    submit_purchase(driver)
    assert "Thank you" in driver.page_source

def test_skn_14_negatif_logika_bulan_invalid(driver):
    go_to_purchase(driver)
    driver.find_element(By.ID, "creditCardMonth").clear()
    driver.find_element(By.ID, "creditCardMonth").send_keys("13")
    submit_purchase(driver)
    assert "confirmation.php" in driver.current_url

# ==========================================
# SKN-15: Kehadiran Tahun Kedaluwarsa
# ==========================================
def test_skn_15_positif_input_tahun(driver):
    go_to_purchase(driver)
    driver.find_element(By.ID, "creditCardYear").clear()
    driver.find_element(By.ID, "creditCardYear").send_keys("2028")
    submit_purchase(driver)
    assert "Thank you" in driver.page_source

def test_skn_15_negatif_kosongkan_tahun(driver):
    go_to_purchase(driver)
    driver.find_element(By.ID, "creditCardYear").clear()
    submit_purchase(driver)
    assert "confirmation.php" in driver.current_url

# ==========================================
# SKN-16: Validasi Logika Tahun (Expired)
# ==========================================
def test_skn_16_positif_tahun_aktif(driver):
    go_to_purchase(driver)
    driver.find_element(By.ID, "creditCardYear").clear()
    driver.find_element(By.ID, "creditCardYear").send_keys("2027")
    submit_purchase(driver)
    assert "Thank you" in driver.page_source

def test_skn_16_negatif_tahun_expired(driver):
    go_to_purchase(driver)
    driver.find_element(By.ID, "creditCardYear").clear()
    driver.find_element(By.ID, "creditCardYear").send_keys("2020")
    submit_purchase(driver)
    assert "confirmation.php" in driver.current_url

# ==========================================
# SKN-17: Kehadiran Nama Pemilik Kartu
# ==========================================
def test_skn_17_positif_input_nama_kartu(driver):
    go_to_purchase(driver)
    driver.find_element(By.ID, "nameOnCard").send_keys("John Doe")
    submit_purchase(driver)
    assert "Thank you" in driver.page_source

def test_skn_17_negatif_kosongkan_nama_kartu(driver):
    go_to_purchase(driver)
    driver.find_element(By.ID, "nameOnCard").clear()
    submit_purchase(driver)
    assert "confirmation.php" in driver.current_url

# ==========================================
# SKN-18: Validasi Format Nama Kartu
# ==========================================
def test_skn_18_positif_format_nama_kartu_huruf(driver):
    go_to_purchase(driver)
    driver.find_element(By.ID, "nameOnCard").send_keys("Amay")
    submit_purchase(driver)
    assert "Thank you" in driver.page_source

def test_skn_18_negatif_format_nama_kartu_angka(driver):
    go_to_purchase(driver)
    driver.find_element(By.ID, "nameOnCard").send_keys("12345678")
    submit_purchase(driver)
    assert "confirmation.php" in driver.current_url

# ==========================================
# SKN-19: Uji Batas Karakter (Boundary)
# ==========================================
def test_skn_19_positif_karakter_wajar(driver):
    go_to_purchase(driver)
    driver.find_element(By.ID, "inputName").send_keys("A" * 50)
    submit_purchase(driver)
    assert "Thank you" in driver.page_source

def test_skn_19_negatif_karakter_berlebih(driver):
    go_to_purchase(driver)
    driver.find_element(By.ID, "inputName").send_keys("A" * 5000)
    submit_purchase(driver)
    assert "confirmation.php" in driver.current_url

# ==========================================
# SKN-20: Uji Keamanan (XSS)
# ==========================================
def test_skn_20_positif_input_standar(driver):
    go_to_purchase(driver)
    driver.find_element(By.ID, "inputName").send_keys("Input Standar")
    submit_purchase(driver)
    assert "Thank you" in driver.page_source

def test_skn_20_negatif_input_xss(driver):
    go_to_purchase(driver)
    driver.find_element(By.ID, "inputName").send_keys("<script>alert(1)</script>")
    submit_purchase(driver)
    assert "confirmation.php" in driver.current_url
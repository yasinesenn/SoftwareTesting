import os
from unittest.mock import mock_open, patch
from django.http import HttpRequest
from django.test import Client, RequestFactory, TestCase
from django.urls import reverse
from parameterized import parameterized
from YazilimTest.fileOperations import codeLine_Counter, find_function_comments, getAllLines_Count, getAlllines_Count, getCommentDeviation_Perc, getJavadoc_Count, getMultiLine_Count, getSingleLine_Count, read_Java_Files, readWithpath
from YazilimTest.forms import GitHubDepoForm
from YazilimTest.gitOperations import clean_clone_directory
from YazilimTest.views import github_depo_ekle, github_repo_list
from .models import JavaClass, GitHubDepo
from faker import Faker

class JavaClassTestCase(TestCase):
    def setUp(self):
        # Test GitHubDepo 
        self.github_repo = GitHubDepo.objects.create(url="https://github.com/example/repo")

        # Test JavaClass 
        self.java_class = JavaClass.objects.create(
            github_repo=self.github_repo,
            class_name="TestClass",
            javadoc_lines_count=10,
            comment_lines_count=20,
            code_line_count=50,
            loc_count=70,
            function_count=5,
            comment_deviation_perc=25.0
        )

    # java classlarinin duzgun olusturulup olusturulmadıgını kontrol eder. 1
    def test_java_class_creation(self):
        self.assertEqual(self.java_class.class_name, "TestClass")
        self.assertEqual(self.java_class.javadoc_lines_count, 10)
        self.assertEqual(self.java_class.comment_lines_count, 20)
        self.assertEqual(self.java_class.code_line_count, 50)
        self.assertEqual(self.java_class.loc_count, 70)
        self.assertEqual(self.java_class.function_count, 5)
        self.assertEqual(self.java_class.comment_deviation_perc, 25.0)

    #str methodunun calisip calismadigini kontrol eder. 2
    def test_str_method(self):
        self.assertEqual(str(self.java_class), "TestClass")

    #sapma hesaplama fonksiyonunun kontrolu  3 
    def test_get_comment_deviation_perc(self):
        javadoc = 5
        comment = 10
        function_count = 3
        code_lines = 50

        result = getCommentDeviation_Perc(javadoc, comment, function_count, code_lines)
        
        expected_result = ((100 * (((javadoc + comment) * 0.8) / function_count)) / ((code_lines / function_count) * 0.3)) - 100

        self.assertAlmostEqual(result, expected_result, places=5)
    
    #CodeLines Fonksiyonu kontrolu
    def test_code_with_comments(self):
        str = readWithpath("YazilimTest/fakeJavaFiles/Hesap.java")

        result = codeLine_Counter(str)
        self.assertEqual(result, 35)

    #getJavadoc_Count Fonksiyonu kontrolu
    def test_getJavadoc_Count(self):
        str = readWithpath("YazilimTest/fakeJavaFiles/Hesap.java")
        result = getJavadoc_Count(str)
        self.assertEqual(result, 3) 

    #getAllLines_Count Fonksiyonu kontrolu
    def test_getAllLines_Count(self):
        str = readWithpath("YazilimTest/fakeJavaFiles/Program.java")
        result = getAllLines_Count(str)
        self.assertEqual(result, 33) 

    #test_getSingleLine_Count icin test
    def test_getSingleLine_Count(self):
        str = readWithpath("YazilimTest/fakeJavaFiles/Program.java")
        result = getSingleLine_Count(str)
        self.assertEqual(result, 5)  # Tek satırlı yorum sayısı

    # functionCount 0 olursa tanimsiz olacagi icin test
    def test_getCommentDeviation_Perc_zero_function_count(self):
        javadoc = 5
        comment = 10
        function_count = 0
        code_lines = 4
        result = getCommentDeviation_Perc(javadoc, comment, function_count, code_lines)
        self.assertEqual(result, 0)

    #hepsi 0 olursa icin test
    def test_getCommentDeviation_Perc_zero_all(self):
        javadoc = 0
        comment = 0
        function_count = 0
        code_lines = 0
        result = getCommentDeviation_Perc(javadoc, comment, function_count, code_lines)
        self.assertEqual(result, 0)

    #javacode Test
    def test_code_with_comments(self):
        str = readWithpath("YazilimTest/fakeJavaFiles/Program.java")

        result = codeLine_Counter(str)
        self.assertEqual(result, 18)

    def test_getMultiLine_Count(self):
        str = readWithpath("YazilimTest/fakeJavaFiles/Program.java")
        result = getMultiLine_Count(str)
        self.assertEqual(result, 1)  # Çok satırlı yorum sayısı


    #test_getSingleLine_Count icin test
    def test_getSingleLine_Count(self):
        str = readWithpath("YazilimTest/fakeJavaFiles/Hesap.java")
        result = getSingleLine_Count(str)
        self.assertEqual(result, 3)  # Tek satırlı yorum sayısı

    #test_readWithpath_success icin test
    def test_readWithpath_success(self):
        file_path = 'test_file.txt'
        expected_content = 'Test file content'
        with patch('builtins.open', mock_open(read_data=expected_content)) as mock_file:
            result = readWithpath(file_path)
            mock_file.assert_called_once_with(file_path, 'r')
            self.assertEqual(result, expected_content)

    #test_readWithpath_file_not_found icin test
    @patch('builtins.print')
    def test_readWithpath_file_not_found(self, mock_print):
        file_path = 'non_existent_file.txt'
        result = readWithpath(file_path)
        mock_print.assert_called_once_with(f"Dosya bulunamadı: {file_path}")
        self.assertIsNone(result)
    
    
    # codelines 0 olursa tanimsiz olacagi icin test
    def test_getCommentDeviation_Perc_zero_code_lines(self):
        javadoc = 5
        comment = 10
        function_count = 3
        code_lines = 0
        result = getCommentDeviation_Perc(javadoc, comment, function_count, code_lines)
        self.assertEqual(result, 0)

#parametrized Test
class TestGetCommentDeviation(TestCase):
    def setUp(self):
        self.test_cases = [
            # Test verileri: (javadoc, comment, function_count, code_lines, expected_result)
            (5, 10, 3, 0, 0),  
            (10, 20, 5, 20, 300),  
            (17, 21, 31, 7, 1347.619047619048),
            
        ]

    def test_getCommentDeviation_Perc(self):
        for javadoc, comment, function_count, code_lines, expected_result in self.test_cases:
            with self.subTest(javadoc=javadoc, comment=comment, function_count=function_count, code_lines=code_lines, expected_result=expected_result):
                result = getCommentDeviation_Perc(javadoc, comment, function_count, code_lines)
                self.assertEqual(result, expected_result)


    def test_getAllLines_Count(self):
        test_cases = [
            ("YazilimTest/fakeJavaFiles/Program.java", 33),
            ("YazilimTest/fakeJavaFiles/Hesap.java", 53),
        ]

        for file_path, expected_count in test_cases:
            with self.subTest(file_path=file_path, expected_count=expected_count):
                str_content = readWithpath(file_path)
                result = getAllLines_Count(str_content)
                self.assertEqual(result, expected_count)


class TestViews(TestCase):
    def setUp(self):
        self.client = Client()

    
    @parameterized.expand([
        ("url1 - bos URL", ""),  # Boş URL
        ("url2 - Gecersiz Url", "merhabaSoftwareTesting"),  # Geçersiz URL formatı
        ("url3 - Gecersiz Url Format", "denemeTesting"),
        ("url4 - sacmaFormat", "buCalismayacak"),
    ])
    def test_request_failure(self, name, github_repo_url):
        response = self.client.post(reverse('anasayfa'), {'url': github_repo_url})

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'getRepoURL.html')
        self.assertFalse(GitHubDepo.objects.filter(url=github_repo_url).exists())




    @parameterized.expand([
        ("url1", "https://github.com/mfadak/Odev1Ornek.git"),
        ("url2", "https://github.com/mfadak/Java_Programming.git"),
        ("url3", "https://github.com/mfadak/Odev1Ornek.git"),
        ("url3", "https://github.com/yasinesenn/programlama_dillerinin_prensipleri1.git"),
        
    ])
    def test_request_success(self, name, github_repo_url):
        response = self.client.post(reverse('anasayfa'), {'url': github_repo_url})

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')
        self.assertTrue(GitHubDepo.objects.filter(url=github_repo_url).exists())




class TestGetAllLinesCount(TestCase):

    @parameterized.expand([
        ("Empty_File", " class test \n merhaba \n software testing", 3),
        ("Single_Line", "public class Program {", 1),
        ("Multiple_Lines", "public class Program {\n    public static void main(String[] args) {\n        System.out.println(\"Hello, World!\");\n    }\n}", 5),
        ("Special_Characters", "!@#$%^&*()_+=-{}[]|;:',.<>?/", 1)
    ])
    def test_getAllLines_Count(self, name, java_code, expected_count):
        result = getAlllines_Count(java_code)
        self.assertEqual(result, expected_count)

    
  
    @parameterized.expand([
        ("Test 1", "gecersiz.txt"),
        ("Test 2", "gecersiz2.txt"),
        
    ])
    @patch('builtins.print')
    def test_readWithpath_file_not_found(self, name, file_path, mock_print):
        result = readWithpath(file_path)
        mock_print.assert_called_once_with(f"Dosya bulunamadı: {file_path}")
        self.assertIsNone(result)


class TestGetSingleLineCount(TestCase):

    def setUp(self):
        self.fake = Faker()

    def test_getSingleLine_Count(self):

        fake_comment = self.fake.sentence()
        java_code = f"public class Test {{\n\t// {fake_comment}\n\tpublic static void main(String[] args) {{\n\t\tSystem.out.println('Hello, world!');\n\t}}\n}}"
        print(fake_comment)
     
        result = getSingleLine_Count(java_code)
        
       
        self.assertEqual(result, 1)
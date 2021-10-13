import INDDate_Defs as pf
import urllib.request

def all_pdf(url, all_vall):
    urllib.request.urlretrieve(url, "../IND1.pdf")  # Скачиваем ПДФ

    all_vall = pf.extract_text('../IND1.pdf', pf.all_patterns, all_vall)
    all_vall = pf.correct_time(all_vall)
    return all_vall


if __name__ == "__main__":
    all_vall = []  # Создаём пустой список
    for i in range(len(pf.all_patterns)):
        all_vall.append('')

    # Проверенные ссылки на пдф
    url = 'https://www.accessdata.fda.gov/drugsatfda_docs/nda/2013/202971Orig1s000PharmR.pdf'  # с инд, датой и индикацией
    # url = 'https://www.accessdata.fda.gov/drugsatfda_docs/nda/2021/212887Orig1s000,212888Orig1s000Approv.pdf' # с инд (6)
    # url = 'https://www.accessdata.fda.gov/drugsatfda_docs/nda/2012/202428Orig1s000PharmR.pdf'                 # с инд (6)
    # url = 'https://www.accessdata.fda.gov/drugsatfda_docs/nda/2002/21-456_Aciphex_Medr_P1.pdf'                # Картинка с датой IND, но без номера
    # url = 'https://www.accessdata.fda.gov/drugsatfda_docs/nda/2010/022518Orig1s000PharmR.pdf'                   # Куча разных номеров инд с датой
    # url = "https://www.accessdata.fda.gov/drugsatfda_docs/nda/2017/208610Orig1s000,208611Orig1s000MedR.pdf"     # Индикация

    all_vall = all_pdf(url, all_vall)
    print(all_vall)
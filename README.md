VaccineSLotNotifier

VaccineSLotNotifier checks the cowin portal periodically to find
vaccination slots available in your district with the age filter already
inserted.. Whenever found, it will send you emails every minute until
the slots are available for that particular district selected. You can
also update the period of receiving emails in the given code.

Steps to Run the code in the local machine: 1.Download Python:
https://www.python.org/ftp/python/3.9.4/python-3.9.4-amd64.exe

2.Open Command Prompt from the search bar and run the following cmd's:
-\> python --version -\> pip --version -\> pip install cachetools -\>
pip install pandas -\> pip install requests -\> pip install retry

3.Open the vaccinetrackingtrigger.py file in the notepade++, make the
below necessary changes according to the requirement:
* ([Line 112](https://github.com/ritusedani/vaccineslotnotifier/blob/4a11996d909edc2375cda691ec0520ac5f39e560/vaccinetrackingtrigger.py#L112))  : server.login(sender_email, "Enter Your App Password")
        To set your App Password ,refer this document:  https://support.google.com/accounts/answer/185833?p=InvalidSecondFactor&visit_id=637554658548216477-2576856839&rd=1
        [Please note that try not use your MAIN GMAIL ACCOUNT FOR THIS PURPOSE- try making a another gmail account for such purposes to avoid any Cyber crime/Hacking]

* ([Line 122](https://github.com/ritusedani/vaccineslotnotifier/blob/4a11996d909edc2375cda691ec0520ac5f39e560/vaccinetrackingtrigger.py#L122))  : #Enter the districts with district id in the given format and include that component in dist_ids:
        The file named districts.csv is attached along with it. Refer to your district and its Id and paste it in the given format as given in the code.
        You can add multiple cities also.

* ([Line 128](https://github.com/ritusedani/vaccineslotnotifier/blob/4a11996d909edc2375cda691ec0520ac5f39e560/vaccinetrackingtrigger.py#L128))  : sender_email="xyz@gmail.com"
        Enter the gmail to which you have set the App Password 

* ([Line 129](https://github.com/ritusedani/vaccineslotnotifier/blob/4a11996d909edc2375cda691ec0520ac5f39e560/vaccinetrackingtrigger.py#L129))  : receiver_email_1 = "abc@gmail.com"
        Enter the gmail where you want to receive updates for vaccination slots.
        You can enter the same email address as os sender_email as given above.

* ([Line 134](https://github.com/ritusedani/vaccineslotnotifier/blob/4a11996d909edc2375cda691ec0520ac5f39e560/vaccinetrackingtrigger.py#L134))  : s.enter(60, 1, do_something, (sc,)) 
        60= You can change the integer value according to your requirement. It represents the time period which will trigger the email update if any slot is found.

4.Open the folder where the .py file is stored, Run the cmd command on
the directory and write: -\> python vaccinetrackingtrigger.py

5.To close the triggering updates, simply close the command prompt and
you good to go.


![MailSS](https://user-images.githubusercontent.com/83569942/116973094-a7524700-acd9-11eb-90e3-4638f06000a0.PNG)

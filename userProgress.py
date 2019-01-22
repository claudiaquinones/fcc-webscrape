from selenium import webdriver
import time
import config

# Access freeCodeCamp website
url = "https://learn.freecodecamp.org/"
driver = webdriver.Firefox()
driver.get(url)

# Locate and click the sign in button contained in the navigation bar
button = driver.find_element_by_class_name("sign-in-btn")
button.click()
time.sleep(3)

# Get the window handle after a new window has opened, and switch
window_after = driver.window_handles[1]
driver.switch_to.window(window_after)

# Locate and click the Google sign in option
login = driver.find_element_by_id("login-google")
login.click()
time.sleep(3)

# Find the email address input, fill it out, then submit
email = driver.find_element_by_id("identifierId")
email.send_keys(config.EMAIL)
email_button = driver.find_element_by_class_name("RveJvd")
email_button.click()
time.sleep(3)

# Find the password input, fill it out, then submit
pass_value = driver.find_element_by_class_name("whsOnd")
pass_value.click()
pass_value.send_keys(config.PASS)
button = driver.find_element_by_class_name("RveJvd")
button.click()

# Now the user should be logged into their account
# The program will now collect some general information on the user's progress and write it to a file
data = driver.find_elements_by_class_name("stats")
file = open("userOverview.csv", "w")
file.write("Complete,Incomplete\n")

for value in data:
    completed_task = int(value.find_elements_by_class_name("green-text")[0].text)
    incomplete_task = int(value.find_elements_by_class_name("green-text")[1].text) - completed_task

    file.write(str(completed_task) + "," + str(incomplete_task) + "\n")
file.close()

# And now the program will travel to the curriculum page to obtain more data on the user's progress
curriculum = driver.find_element_by_xpath("/html/body/nav/div[2]/ul/li[1]/a")
curriculum.click()

# FCC automatically opens the Responsive Web Design Cert. and the first sub-topic
# Close these links
basic_html_and_html5_link = driver.find_element_by_tag_name("h5")
basic_html_and_html5_link.click()  # Close

responsive_web_design_cert_link = driver.find_element_by_tag_name("h4")
responsive_web_design_cert_link.click()  # Close

# Find all main topics
main_topics = driver.find_elements_by_tag_name("h4")

f = open("userCurriculum.csv", "w")
f.write("Topic,Challenges,Completed\n")

# The program will now open all the main topic links and collect how many challenges there are per main topic and
# how many the user has completed
total_challenges = 0
for topic in main_topics:
    topic.click()  # Open main topic link
    sub_topics = driver.find_elements_by_tag_name("h5")  # Find all sub-topics

    completed_challenges = 0
    sub_challenges = 0
    for sub_topic in sub_topics:
        sub_topic.click()  # Open

        challenges = driver.find_elements_by_class_name("map-challenge-title")
        total_challenges = len(challenges) - 1 + total_challenges
        sub_challenges += len(challenges) - 1

        status_of_challenges = driver.find_elements_by_class_name("sr-only")
        for challenge in status_of_challenges:
            if challenge.text == 'Passed':
                completed_challenges += 1

        sub_topic.click()  # Close
    topic_string = topic.text.replace(" Certification (300 hours)", "")
    topic_string = topic_string.replace(" (Thousands of hours of challenges)", "")

    f.write(topic_string + "," + str(sub_challenges) + "," + str(completed_challenges) + "\n")
    topic.click()  # Close main topic

print("Total challenges: ", total_challenges)
driver.close()
f.close()

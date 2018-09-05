import requests
from selenium import webdriver


url = "https://learn.freecodecamp.org/"
driver = webdriver.Firefox()
driver.get(url)

# FCC automatically opens the Responsive Web Design Cert. and the first sub-topic
# Close these links
basic_html_and_html5_link = driver.find_element_by_tag_name("h5")
basic_html_and_html5_link.click() # close

responsive_web_design_cert_link = driver.find_element_by_tag_name("h4")
responsive_web_design_cert_link.click() # close

# Find all main topics
main_topics = driver.find_elements_by_tag_name("h4")

filename = "fcc-Challenges.csv"
f = open(filename, "w")
f.write("Topic, Sub-topic, Challenges\n")

sum = 0

for topic in main_topics:
    topic.click() # open main topic link
    sub_topics = driver.find_elements_by_tag_name("h5") # find all sub-topics
    print("\n", topic.text, ":")
    for sub_topic in sub_topics:
        sub_topic.click()
        challenges = driver.find_elements_by_class_name("map-challenge-title")
        sum = len(challenges) - 1 + sum
        print("\t", sub_topic.text, ":", len(challenges) - 1 )

        sub_topic.click() # close
        topic_string = topic.text.replace("Certification (300 hours)", "")
        topic_string = topic_string.replace("(Thousands of hours of challenges)", "")

        f.write(topic_string + "," + sub_topic.text + "," + str(len(challenges) - 1) +  "\n")

    topic.click() # close main topic

print("\n\nTotal challenges ", sum)
driver.close()
f.close()

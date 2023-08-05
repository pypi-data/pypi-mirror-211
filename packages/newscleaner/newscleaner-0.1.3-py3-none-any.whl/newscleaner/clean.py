import re
import json
import html
import unicodedata
import pkg_resources


#  Cleaning raw HTML and retaining tags

def cleaner(text):
    
    tags = {'<p>' : '{p}', '</p>':'{/p}','<span>': '{span}','</span>':'{/span}', '<br>':'{br}','</br>':'{/br}','<b>':'{b}',
       '</b>':'{/b}','<i>':'{i}','</i>':'{/i}','<u>':'{u}','</u>':'{/u}' , '<strong>':'{strong}','</strong>':'{/strong}',
        '<h1>':'{h1}','</h1>':'{/h1}','<h2>':'{h2}','</h2>':'{/h2}', '<h3>':'{h3}','</h3>':'{/h3}','<h4>':'{h4}','</h4>':'{/h4}',
        '<h5>':'{h5}','</h5>':'{/h5}','<h6>':'{h6}','</h6>':'{/h6}', '<td>':'{td}', '</td>': '{/td}', '<tr>':'{tr}', '</tr>': '{/tr}'}
    
    def replace_all(text, dic):
        for i, j in dic.items():
            text = text.replace(i, j)
        return text

    def replace_all1(text, dic):
        for i, j in dic.items():
            text = text.replace(j, i)
        return text

    clean_text = replace_all(text,tags)
    clean_text = re.sub(r'<[^<>]*>', ' ',clean_text) #removing all html tags
    clean_text = re.sub('http[s]?://\S+', ' ',clean_text) # removing all hyperlinks
    clean_text = re.sub('\S*@\S*\s?', '',clean_text) #removing all links
    #clean_text = re.sub(r'[A-Za-z0-9]*@[A-Za-z]*\.?[A-Za-z0-9]*', '',clean_text)
    clean_text = re.sub('\|*Advertisement\|*','',clean_text) #removing Advertisement keyword
    clean_text = re.sub('\|*(Getty Images)\|*','',clean_text) #removing getty images keyword
    clean_text = re.sub('\n|\t|\r','',clean_text) # removing tabs, nextline characters 
    clean_text = re.sub(r"\s+", " ",clean_text)
    clean_text = re.sub(r"\\" ,"",clean_text) #removing backslashes
    clean_text = re.sub("\(.*?\)|\[.*?\]","",clean_text)

    
    # Removing Pattern from independent.uk.co
    clean_text = re.sub(".*" + "r {{ /verifyErrors }}", '',clean_text)
    clean_text = re.sub(".*" + "Washington email" , '',clean_text)
    clean_text = re.sub(".*" + "breaking news emails", '',clean_text) 
    clean_text = re.sub(".*" + "for all the latest news", '',clean_text)
    clean_text = re.sub(".*" + "This email for free", '',clean_text)
    clean_text = re.sub(".*" + "Check email", '',clean_text)
    clean_text = re.sub(".*" + "Headlines email", '',clean_text)
    
    # msnbc pattern removal
    clean_text = re.sub("Tweet us " + ".*",'',clean_text)
    clean_text = re.sub("You can read more" + ".*",'',clean_text)
    
    #greenwich & ourmidland time pattern removal
    clean_text = re.sub("UP NEXT" + ".*" ,'',clean_text)
    clean_text = re.sub("This is a carousel. Use Next and Previous buttons to navigate",'',clean_text)
    clean_text = re.sub("Show More",'',clean_text)
    clean_text = re.sub("Show Less",'',clean_text)
    
    #NJ.com 
    clean_text = re.sub("Our journalism needs your support" + ".*",'',clean_text)
    clean_text = re.sub("For NJ Advance",'',clean_text)
    clean_text = re.sub(r"\|",'.',clean_text)
    clean_text = re.sub("COPYRIGHT 2023 CREATORS.COM",'',clean_text)
    clean_text = re.sub("Thank you for relying on us to provide" + ".*",'',clean_text)
    clean_text = re.sub("RELATED STORIES " + ".*",'',clean_text)
    clean_text = re.sub("The N.J. High School Sports newsletter" + ".*",'',clean_text)
    
    #nbcsports
    clean_text = re.sub("Subscribe to and rate" + ".*",'',clean_text)
    clean_text = re.sub(" Click here to follow the " + ".*",'',clean_text)
    clean_text = re.sub(" Download and follow the" + ".*",'',clean_text)

    #newsweek
    clean_text = re.sub("Getty",'',clean_text)
    clean_text = re.sub("Newsweek reached out to" + ".*",'',clean_text)
    clean_text = re.sub("Newsweek has reached out to" + ".*",'',clean_text)
    
    #click2houston
    #pattern_c2 = "___" + ".*"
    #clean_text = re.sub(pattern_c2,'',clean_text)
    
    #clickorlando
    clean_text = re.sub("Get today’s headlines in minutes with",'',clean_text)
    clean_text = re.sub("Your Florida Daily",'',clean_text)
    clean_text = re.sub(":",'',clean_text)
    clean_text = re.sub("Click here for more information about" + ".*",'',clean_text)
    clean_text = re.sub("FILE - ",'',clean_text)
    
    #cleveland.com
    clean_text = re.sub(" See video of the play here ",'',clean_text)
    clean_text = re.sub("\*",'',clean_text)
    clean_text = re.sub("Get police blotters by email every weekday for free with our new Police Blotter newsletter."  + ".*",'',clean_text)
    clean_text = re.sub("Ad not displaying properly?" + ".*",'',clean_text)
    clean_text = re.sub("Get a jumpstart on the weekend. Sign up for Cleveland.com ’s" + ".*",'',clean_text)
    clean_text = re.sub("Read more of her work" + ".*",'',clean_text)
    
    #nbcboston
    clean_text = re.sub("Get Boston local news, weather forecasts, lifestyle and entertainment stories to your inbox.","",clean_text)
    clean_text = re.sub("’s newsletters.","",clean_text)
    clean_text = re.sub("Read the full story on NBCNews.com here.","",clean_text)
    clean_text = re.sub("PHOTOS","",clean_text)
    clean_text = re.sub(r'pic\.twitter\.com/\w+', '',clean_text) #removing twitter patterns
    clean_text = re.sub("Get Boston local news, weather forecasts, lifestyle and entertainment stories to your inbox. ’s newsletters.",'',clean_text)
    
    #nbcchicago
    clean_text = re.sub("Get Chicago local news, weather forecasts, sports and entertainment stories to your inbox.","",clean_text)
    clean_text = re.sub("Read the full story on NBCNews.com here.","",clean_text)
    clean_text = re.sub("PHOTOS:","",clean_text)
    clean_text = re.sub("Download MyTeams Today!","",clean_text)
    clean_text = re.sub("Click here to"+".*","",clean_text)
    clean_text = re.sub("Be sure to download the NBC Chicago app on your Apple or Android devices , or you can tune into the NBC 5 newscasts throughout the afternoon for the latest weather information.","",clean_text)
    clean_text = re.sub("For all the latest information, stay tuned to the NBC"+".*",'',clean_text)
    
    #nbcdfw
    clean_text = re.sub("Read the full story at NBCNews.com","",clean_text)
    clean_text = re.sub("Editor's note: All odds are provided by our partner, PointsBet ."+".*","",clean_text)
    clean_text = re.sub(" This story first appeared on TODAY.com . More from TODAY: ","",clean_text)
    
    #cnbc 
    clean_text = re.sub("Subscribe\xa0 here \xa0to get this report sent directly to your inbox each morning before markets open. ","",clean_text)
    clean_text = re.sub("watch now","",clean_text)
    clean_text = re.sub("Getty Images Entertainment | Getty Images","",clean_text)
    
    #wgntv
    clean_text = re.sub("Suggest a Correction","",clean_text)
    clean_text = re.sub("This is a developing story, follow"+".*","",clean_text)
    
    #fox2news
    clean_text = re.sub("You can find out more at"+".*","",clean_text)
    clean_text = re.sub("Photo: ","",clean_text)
    clean_text = re.sub("This story will be updated throughout the day.","",clean_text)
    clean_text = re.sub(r'[()]', '',clean_text)
    clean_text = re.sub(r"The Conversation","",clean_text)
    clean_text = re.sub(r'(-)+', r'\1',clean_text)
    #clean_text = re.sub(r"( ) – ","",clean_text)
    
    #nbcmiami
    clean_text = re.sub("Get South Florida local news, weather forecasts and entertainment stories to your inbox.","",clean_text)
    clean_text = re.sub(" More information on how to apply can be found here .","",clean_text)
    clean_text = re.sub("This story first appeared on TODAY.com."+".*","",clean_text)
    
    clean_text = re.sub('\|*(Image source, )\|*','',clean_text) #removing bbc errors
    clean_text = re.sub('\|*(Image caption, )\|*','',clean_text) #removing bbc errors
    clean_text = re.sub('\|*(More on this story)\|*.+','',clean_text) #removing bbc errors
    clean_text = re.sub('\|*(Sign up for )\|*[a-z\sA-Z]+','',clean_text) #removing bbc errors
    clean_text = re.sub('\|*(Sign up to )\|*[a-z\sA-Z]+','',clean_text) #removing bbc errors
    
    clean_text = re.sub('\|*(This content is created and maintained by a third party, )\|*.+','',clean_text) #removing cosmopliton error
    clean_text = re.sub('\|*(Download it for )\|*[a-z\sA-Z]+','',clean_text) #removing cosmopliton error
    clean_text = re.sub('({Android})','{}',clean_text) #removing cosmopliton error
    #clean_text = re.sub('(Follow )+\S+( on ).+','') #removing cosmopliton error
    #clean_text = re.sub('(>Instagram<)','><') #removing Advertisement keyword
    
    clean_text = re.sub('\|*(A version of this story appeared in the )\|*[a-z\sA-Z0-9.]+','',clean_text) #removing hollywood error
    clean_text = re.sub('\|*(Click here to subscribe.)\|*','',clean_text) #removing hollywood error
    
    clean_text = re.sub('\|*(For weekly email updates on\nresidential real estate news, )\|*.+','',clean_text) #removing nytimes error
    
    clean_text = re.sub("\|*(More News)\|*[a-z</>\sA-Z'-.0-9:_‘’|“”$–?.-…{}]+",'',clean_text) #removing stamfordadvocate error
    clean_text = re.sub("\|*(More Entertainment)\|*[a-z</>\sA-Z'-.0-9:_‘’|“”$–?.-…{}]+",'',clean_text) #removing stamfordadvocate error
    clean_text = re.sub("\|*(UP NEXT)\|*[a-z</>\sA-Z'-.0-9:_‘’|“”$–?.-…{}]+",'',clean_text) #removing stamfordadvocate error
    clean_text = re.sub("\|*(___)\|*[a-z</>\sA-Z'-.0-9:_‘’|“”$–?.-…{}]+",'',clean_text) #removing stamfordadvocate error
    clean_text = re.sub('\|*(This is a carousel. Use Next and Previous buttons to navigate)\|*','',clean_text) #removing stamfordadvocate error
    
    #clean_text = re.sub("\|*(Top news)\|*[a-z</>\sA-Z'-.0-9:_‘’|“”$–?.-…{}]+",'',clean_text) #removing thegurdian error
                     
    clean_text = re.sub('\|*(Required reading)\|*','',clean_text) #removing theatheletic error
    clean_text = re.sub("\|*(GO DEEPER{)\|*[/}a-zA-Z\s,'0-9:]+",'',clean_text) #removing theatheletic error
    
    clean_text = re.sub("\|*([A-Z])\|*[A-Z0-9\s',:.-]{20,}",'',clean_text) #removing foxnews error
    clean_text = re.sub("(NEW{)+[/a-zA-Z\s}!]+",'',clean_text) #removing foxnews error
    
    clean_text = re.sub('(}[\s]*Advertising[\s]*{)','}{',clean_text) #removing france24 error
    clean_text = re.sub('(}[\s]*©[\sA-Za-z0-9,/]*{)','}{',clean_text) #removing france24 error
    clean_text = re.sub('({p}[\s]*\(REUTERS\)[\s]*{)([.a-zA-Z0-9/<>!,-_\s]*)','',clean_text) #removing france24 error
    clean_text = re.sub('({p}[\s]*\(AFP\)[\s]*{)([.a-zA-Z0-9/<>!,-_\s]*)','',clean_text) #removing france24 error
    
    clean_text = re.sub("""({/p}[\s]*Get[.a-zA-Z0-9/<>!,{}'"%-’“”_\s]*Enter Email[\s])""",'',clean_text) #removing bostonglobe error
    
    #if "edition.cnn" in df['content_url']:
     #   clean_text = re.sub("""([.a-zA-Z0-9/<>!,{}'"%-’“”_\s]*{/p}[\s]*—[\s]*{/p})""",'{/p}',clean_text) #removing edition.cnn error
    
    clean_text = re.sub("""({p}[\s]*RELATED:[\sA-Za-z/<>!,.'"‘“”_%-]*{/p})""",'',clean_text) #removing nbcnewyork error
    clean_text = re.sub("""({p} This story first appeared on TODAY.com . More from TODAY: {/p})""",'',clean_text) #removing nbcnewyork error
    clean_text = re.sub("""(Get Tri-state area news and weather forecasts to your inbox. Sign up for NBC New York newsletters.)""",'',clean_text) #removing nbcnewyork error
    
    clean_text = re.sub("""({p}[\s]*RELATED:[\sA-Za-z/<>!,.'"‘“”_%-]*{/p})""",'',clean_text) #removing nbcphiladelphia error
    clean_text = re.sub("""({p} This story first appeared on TODAY.com . More from TODAY: {/p})""",'',clean_text) #removing nbcphiladelphia error
    clean_text = re.sub("""(Get Philly local news, weather forecasts, sports and entertainment stories to your inbox. Sign up for NBC Philadelphia newsletters.)""",'',clean_text) #removing nbcphiladelphia error
    
    clean_text = re.sub("""({p}[\s]*RELATED:[\sA-Za-z/<>!,.'"‘“”_%-]*{/p})""",'',clean_text) #removing nbcsandiego error
    clean_text = re.sub("""({p} This story first appeared on TODAY.com . More from TODAY: {/p})""",'',clean_text) #removing nbcsandiego error
    clean_text = re.sub("""(Get San Diego local news, weather forecasts, sports and lifestyle stories to your inbox. Sign up for NBC San Diego newsletters.)""",'',clean_text) #removing nbcsandiego error
    
    #India Cleaning
    clean_text = re.sub('(}[\s]*Advertising[\s]*{)','}{',clean_text) #removing "Advertising" keyword
    clean_text = re.sub("""([\s]*Also read[\s]*{/p})+[a-zA-Z{}=".\s\d&#;,|<>:_'].+({/p})""",'',clean_text) #removing one para after "Also read" keyword
    clean_text = re.sub('(For more lifestyle news).+','',clean_text) #removing text after "For more lifestyle news" keyword
    clean_text = re.sub('(}[\s]*\(With inputs from agencies\)[\s]*{)','}{',clean_text) #removing "(With inputs from agencies)" keywords
    clean_text = re.sub('(({p}[\s]*Read)+[a-zA-Z{}=".\s\d&#;,<>]+(on The Eastern Herald.))+[a-zA-Z{}=".\s\d&#;,<>]+','',clean_text) #removing Last Lines in Eastern Herald keyword
    clean_text = re.sub("""(\{p\}\{strong\}[\s]*Also Read \|)+[a-zA-Z{}=".\s\d&#;,<>:_']+\{/strong\}\{\/p\}""",'',clean_text) #removing one para after "Also Read" keyword
    clean_text = re.sub("""({p}[\s]*SHARE THIS ARTICLE ON[\s]*{/p})+[a-zA-Z{}=".\s\d&#;,*^@$!()+\[\]~`<>:_'\n?%]+""",'',clean_text) #removing text after "SHARE THIS ARTICLE ON" keyword
    clean_text = re.sub("""(\([\s]*Also read \|)+[a-zA-Z{}=".\s\d&#;,<>:_']+(\))""",'',clean_text) #removing one para after "Also read |" keyword
    clean_text = re.sub("""(Also read:)+[a-zA-Z{}=".\s\d&#;,<>:_']+({/a}{/p})""",'',clean_text) #removing one para after "Also read:" keyword
    clean_text = re.sub("""(ALSO READ:)+[a-zA-Z{}=".\s\d&#;,<>:_']+({/a}{/p})""",'',clean_text) #removing one para after "ALSO READ: " keyword
    clean_text = re.sub("""(Also Read:)+[a-zA-Z{}=".\s\d&#;,<>:_']+({/a})""",'',clean_text) #removing one para after "ALSO READ: " keyword
    clean_text = re.sub("""(Also read \|)+[a-zA-Z{}=".\s\d&#;,<>:_'?]+({/a})""",'',clean_text) #removing one para after "Also read |" keyword
    clean_text = re.sub("""([\s]*Source:)+[\sA-Za-z.]+""",'',clean_text) #removing "Source:" keyword
    clean_text = re.sub("""(}[\s]*top videos[\s]*{/p})""",'}',clean_text) #removing "top videos" keyword
    clean_text = re.sub("""(ALSO READ\|)+[a-zA-Z{}=".\s\d&#;,<>:_'?]+({/a})""",'',clean_text) #removing one para after "ALSO READ|" keyword
    clean_text = re.sub("""(}[\s]*Read all the)+[a-zA-Z{}=".\s\d&#;,<>:()_]+(here[\s]*{/p})+[a-zA-Z{}=".\s\d&#;,<>:()_]+""",'}',clean_text) #removing text after "Read all the ... here" keyword
    
    clean_text = re.sub('({p}[\s]*{/p})','',clean_text) #removing empty p-tag keyword
    clean_text = re.sub("""(\{strong\}[\s]*\{\/strong\})""",'',clean_text) #removing empty strong-tag keyword
    clean_text = re.sub('({/a}[\s]*{/a})','',clean_text) #removing empty a-tag keyword
    clean_text = html.unescape(clean_text) #decoding unicode entities using html parser
    clean_text = replace_all1(clean_text,tags) 
    

    
    
    # cleaning emoji
    emoji_pattern = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
        u"\U00002500-\U00002BEF"  # chinese char
        u"\U00002702-\U000027B0"
        u"\U000024C2-\U0001F251"
        u"\U0001f926-\U0001f937"
        u"\U00010000-\U0010ffff"
        u"\u2640-\u2642" 
        u"\u2600-\u2B55"
        u"\u200d"
        u"\u23cf"
        u"\u23e9"
        u"\u231a"
        u"\ufe0f"  # dingbats
        u"\u3030"
                           "]+", flags=re.UNICODE)
    
    clean_text = emoji_pattern.sub(r'', clean_text)
    clean_text = unicodedata.normalize("NFKD",clean_text) #decoding utf-8 unicode data which is producing spacing
    
    # storing words in list with no extra spaces
    clean_text= [j for j in clean_text.strip().split(" ") if j !=""]

    return " ".join(clean_text)
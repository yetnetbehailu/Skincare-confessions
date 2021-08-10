[Chrome DevTools](https://developers.google.com/web/tools/chrome-devtools) - Tool consistently used to identify issues arising and to test changes made throughout site development to ensure web application desired appearance and functionality.

[W3C Markup Validator](https://validator.w3.org/)- Used to validate HTML; No errors found, only warnings implying to the Jinja formatted context.

[W3 CSS Validation Service](https://jigsaw.w3.org/css-validator/#validate_by_input) - Used to validate CSS; No errors found, warnings only implying the use of css prefixes.

[JSLint](https://jslint.com/)- Used to validate Javascript code no major errors found, only warnings in regards to syntax useage(such as using double qoutes, parens around ternery operator & adjusting too long lines)

[Lighthouse](https://chrome.google.com/webstore/detail/lighthouse/blipmdconlkpinefehnmjammfjpmpbjk?hl=en) - Used to test the performance of the application on desktop & mobile.

### Issues and Resolutions

**Errors encountered and resolved during development process**

- First encounter was when trying to display the nav links depending on the user being signed in or not. As my first encounter adapting backend logic to display frontend, I had to do a little reading research to fully understand what needed to be done. Turns out the fix was very simple actually, I would have to create a seesion object to grab the username from database. Once the user has created an account their usename is placed in session cookie and eachtime user tries to log in it's compared to username found in database. Thereafter to render the response from backend onto frontend, curate a jinja statement checking if the session user can be found. To get the accurate display you place the content you want to be viewed when user is signed in or not within the if else statement.

- Another error occured when trying to submit the review form with user inputs using the request.method=='POST'. The form would at such point always submit successfully even knowing input requirements actually had not been meet. This problem occured because the form was not being validated. To make sure the form validators where being checked prior to submission I'd use WTForms library helper validate_on_submit(). The decimal limitation mystery is not as mysterious as in early on. It is still unsolved, but I belive could have been resolved through creating own context processor for the DecimalField to convert the data values in order to be able to modify them in the most accurate way. However current solution adopts the use of Floatfield. It isn't as precise in calculation as decimal128 but works to edit and update the review form. I've tried to configure the float value to only show 2 decimal values by using round() method but that would only round to nearest integer value. Hence have left it as float only.

- The function meant to render the default image, if no image file had been input by user has a particular set up. In the way that the upload img file data is being retrived from the filefiled whilst the default img is actully rendered in html using img tag. However for this instance i've had to use request.form.get in the route logic so the if else statments return accurate response but this shouldn't be a neccesity since the default img url is not being sent & stored in db.

- In regards to the star rating js function determining the coloring depending on rate choice, the first star wouldnt turn yellow on click so I had to adjust the code using more specific selectors for the css styling to work.

- When adapting the flask wtf filefield it comes with a default button which can't be manipulated on its own. Therefore to get the apperance/outcome I wanted I had to create my own custom button to cover the default one provided.

- At some point I had removed the form-control class from the star rating logic, this was a mistake. Because the form control serves as the point of connection between client side and server side handling. A user is able to interact with a form component inputing data that can be sent to server for further processing. It can also affect styling which in this case it did with the star rating field error message positioning.

- The submit event on the add review form was clashing with an attribute with similar (name &/or Id), ending up not submitting the form. This bug was fixed using the HTMLFormElement.prototype.submit.call() method, which submits the (specified) given form element. 

- The html code for the subscription form had a couple of syntax issues at first. One being that I had missed to add the csrf_token, a unique token generated different each time the web page is served. To prevent from malicious web attcks pursuing sensitive user information. The second issue was that I had missplaced the form tag elements.The invalid-feedback bootstrap validation as per requirement needs to be a direct sibling of the the input control to display, hence the adjustment made.

- With the tag input field I was having trouble only creating tags wich contained written context, removing any whitespace symbol as sole input. This however i managed to overcome by replacing(replace() method) any whitespace symbol with an empty string & then checking tag len making sure its greater then the value 0.

- Another situation causing trouble was an indentation slip causing the default img on edit form not to update. Once formatted correctly the default img which had been entered could be altered & the route logic retrived accurately.

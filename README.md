# FaceTouchDetector
Face Touch Detector Readme
Vision:
To give power of life to the masses.

We want to provide the world with a no-cost COVID-19 mitigation tool, which can be implemented by people around the world in minutes.
What is our Product?
A Python-powered application which uses the camera of a computer to notify the user not to touch their face with their hands when they do so. 

The application uses artificial intelligence and machine learning to detect when a user has touched their face, the application then sends a notification and says a sentence warning the user to not touch their face.
What makes our Product Special?
Our product is special since there is no other wide-spread face-touch detection system. Many resources online talk about possible tips and tricks for preventing face-touching, but all rely on the attention and effort of the user. This solution, however, offsets the menial, yet crucial, task to the computer to detect when the user has touched their face and alert the user not to. By having the computer alert the user when the user has touched their face, the user will get trained to not touch his/her face.
Why is this problem important?
One of the main causes of the spread of COVID-19 is people touching their faces frequently. People that have contracted this virus do not show symptoms for up to several days and therefore, it is essential that people avoid touching their faces even if they may think they are not sick.  
How does this project aim to solve the problem?
This app essentially aims to break the common habit of touching one’s face. The notification system reminds the user when they are touching their face, giving them an estimate of how frequently they really repeat this action. Breaking this habit will play a great role in the spread of the virus and will show people that they touch their faces more often than they think.
What was the inspiration?
The inspiration was a combination of two sources. The first was a clip in a youtube video created by Mark Rober which detailed how hard it is for him to not touch his face. The second was from https://experiments.withgoogle.com which showed a project which is able to use a web-camera to notify if a user has a bad posture while using a computer.
What were some challenges we encountered?
We encountered several challenges throughout the development of this app, some of which were overcome and others which we plan to solve post hackathon.

The main challenge was making an AI model that is able to detect where the user’s hand is, not detecting where the user’s face is since there is a prebuilt face detector system in a python library called OpenCV. The biggest problem when creating the AI model was choosing the correct architecture for the model. We went through many iterations and fine-tunings until we found a model, which could predict where a hand or hands are in an image. The second biggest problem was training the AI model on a computer(with no GPU) since the training process was very slow. To solve this problem we were about to use a virtual machine provided by Google to train the model quickly when it dawned upon us to use Google Colab which is able to give us free access to fast training of our models. A slight annoyance was Google Colab’s timeout policy which closed the overnight model training process after 30 minutes of inactivity.
What would we focus on if there was more time?
One feature of our app that we focus on would be the AI model, which could be significantly improved as it sometimes detects that the user is touching their face when they really are not. In addition, we want this model to be smaller and more efficient since there a slight delay between when the user touches their face and when the application notifies the user to not touch their face. Another component of our app that we would direct our focus to is the settings. We want to add a slider that controls the sensitivity of the hand-touching-face algorithm. Additionally, we want to add some customization to the sentence that is said by the application every time the user touches their face as they might eventually get annoyed by the default tone of the computer. 
Who are our target users?
The target user is anybody who has an electronic device with a front-facing camera, so essentially anybody who can access the Internet.
What is our plan for this app post hackathon?
Since we were limited to groups of two in this hackathon, we plan on adding more passionate developers to our group. We already have many features that we listed above to focus on, and more people in our team would certainly help us improve this app at a much quicker pace. The health crisis right now requires immediate action and we want to push out an app as soon as possible so that people can break this habit of touching their hands, effectively helping to prevent the spread of the virus.

Our product is currently only designed for macOS users and we hope to create different versions for Windows, Android, and iOS. With our larger team, it would be much easier to expand to these different platforms and reach a larger number of users.

The current end-goal for the product is a more efficient application which is able to notify the user in a friendly tone to restrain themselves just before their face is touched.

SEE THE ATTACHED PDF FOR PICTURES OF THE APPLICATION

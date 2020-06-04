# vdt
<h3>V. TCO Tool Front End</h3>

This is my first own project in Django, excluding the tutorials and exercises I have done. 
For this reason I am taking notes directly into the code as a way to remember why I had to implent the code the way it is.
I typically indicate this using the code <i>SE_NOTE</i> or <i>SE-NOTE</i>, meaning the commnent is meant to be a Self Educating Note.

As it is right now (1st commit), the code allows to do:
  - Authentication
      + User sign-up
      + User login
      + User logout
  - Design Upload: this upload a file to the model and visualize the content if it is recognized
  - Design Delete: this delete the design (aka project) removing the uploaded file
  - Design Update: this is embedded in the design visualization
  
On the Wuthentication part I will need to add:
  - Password change
  - User delete (but maybe it is safer to have it via Django admin panel)
    
On the Design part:
  - Play with Pandas and Numpys and try to see some output reporting and download
  - Create some output file and save it in a similar way of the input so that we can download it
  

# Django Quiz App

This is a simple Django-based quiz application that fulfills the following functionalities:

1. **Start a New Quiz Session:**  
   The user can begin a new quiz session, which tracks their progress and results.

2. **Get a Random Multiple-Choice Question from the Database:**  
   The app randomly selects a question from the database. Questions are stored in the database as `Question` model instances.

3. **Submit an Answer:**  
   The user can submit their answer, and the app updates their quiz session statistics (total answered, correct, incorrect).

4. **View Quiz Results and Stats:**  
   After completing the quiz or reaching the chosen question limit, the user can view total questions answered, correct/incorrect count, accuracy, and time taken for the quiz.  
   Additionally, the results page shows where questions came from (if `source_url` is provided), allowing the user to learn more about the topic.

## Additional Features

- **Non-Repetitive Questions Until All Seen:**  
  During a session, no question will repeat until all questions have been shown at least once. After cycling through all questions, repetition is allowed.

- **User-Selectable Number of Questions:**  
  The user can choose how many questions to answer in a session (1, 5, 10, 15, 30).

- **Enhanced UI/UX Dashboard:**  
  The result page acts as a dashboard, showing accuracy and time taken. If questions have a `source_url`, the user can easily access further learning materials.

## Assumptions

- Only one user is required (no multi-user handling).
- Questions are stored in the database and can be added either via the Django admin panel or through a management command.
- No separate UI for question creation is required by the assignment (admin panel usage is acceptable).

## Project Structure


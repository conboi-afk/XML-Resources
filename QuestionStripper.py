import sys

def parseQuestions(content):
    questions = []
    questionData = []
    answerBank = []
    for lineNum in range(len(content)):
        if lineNum < len(content):
            # question
            if "pts" in content[lineNum]:
                questions.append(content[lineNum+1])
                for x in range(lineNum+1, len(content)):
                    if "pts" not in content[x]:
                        questionData.append(content[x])
                    else:
                        break
                answerBank.append(questionData)
                questionData = []

    answers = []
    for data in answerBank:
        # mix and match
        if len(data) > 30:
            answers.append("[MC]")
        else:
            for lineNum in range(len(data)):
                # multiple choice, fill in the blank, Correct!
                if "Correct Answer" in data[lineNum] or "Correct Answers" in data[lineNum] or "Correct!" in data[lineNum]:
                    answers.append(data[lineNum+1])
                    break
                # true/false
                elif "You Answered" in data[lineNum] and "True" in data[lineNum+1]:
                    answers.append(data[lineNum+2])
                    break
                elif "Your Answer" in data[lineNum]:
                    answers.append("[Not graded]")

    return [questions, answers]

def outputFile(fileName, questions, answers):
    fileData = fileName.split(".")
    newName = fileData[0] + "_Questions." + fileData[1]
    with open(newName, "w+") as newFile:
        for num in range(len(questions)):
            newFile.write(str(num+1) + ": " + questions[num] + answers[num].strip() + "\n\n")

if len(sys.argv) > 1:
    questionFile = open(sys.argv[1])
    content = parseQuestions(questionFile.readlines())
    outputFile(sys.argv[1], content[0], content[1])

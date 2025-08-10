import turtle

def execute_instructions(filename):
    screen = turtle.Screen()
    screen.title("Instructions Turtle")
    
    t = turtle.Turtle()
    t.speed(0)

    with open(filename, "r") as file:
        for line in file:
            line = line.strip().lower()
            if line.startswith("avance"):
                value = int(line.split()[1])
                t.forward(value)
            elif line.startswith("recule"):
                value = int(line.split()[1])
                t.backward(value)
            elif line.startswith("tourne droite"):
                value = int(line.split()[-2])
                t.right(value)
            elif line.startswith("tourne gauche"):
                value = int(line.split()[-2])
                t.left(value)
            else:
                print(f"Instruction non reconnue : {line}")

    turtle.done()

execute_instructions("turtle")

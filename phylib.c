#include <stdio.h>
#include <math.h>
#include <string.h>
#include <stdlib.h>
#include "phylib.h"

phylib_object *phylib_new_still_ball(unsigned char number, phylib_coord *pos)
{
    phylib_object *new_sb = NULL;
    new_sb = (phylib_object *)malloc(sizeof(phylib_object));
    if (new_sb == NULL)
        return NULL;

    new_sb->type = PHYLIB_STILL_BALL;
    new_sb->obj.still_ball.number = number;
    new_sb->obj.still_ball.pos = *pos;

    return new_sb;
}

phylib_object *phylib_new_rolling_ball(unsigned char number, phylib_coord *pos, phylib_coord *vel, phylib_coord *acc)
{
    phylib_object *new_rb = NULL;
    new_rb = (phylib_object *)malloc(sizeof(phylib_object));
    if (new_rb == NULL)
        return NULL;

    new_rb->type = PHYLIB_ROLLING_BALL;
    new_rb->obj.rolling_ball.number = number;
    new_rb->obj.rolling_ball.pos = *pos;
    new_rb->obj.rolling_ball.vel = *vel;
    new_rb->obj.rolling_ball.acc = *acc;
    return new_rb;
}

phylib_object *phylib_new_hole(phylib_coord *pos)
{
    phylib_object *new_hole = NULL;
    new_hole = (phylib_object *)malloc(sizeof(phylib_object));
    if (new_hole == NULL)
        return NULL;

    new_hole->type = PHYLIB_HOLE;
    new_hole->obj.hole.pos = *pos;

    return new_hole;
}
phylib_object *phylib_new_hcushion(double y)
{
    phylib_object *new_HC = NULL;
    new_HC = (phylib_object *)malloc(sizeof(phylib_object));
    if (new_HC == NULL)
        return NULL;

    new_HC->type = PHYLIB_HCUSHION;
    new_HC->obj.hcushion.y = y;

    return new_HC;
}
phylib_object *phylib_new_vcushion(double x)
{
    phylib_object *new_VC = NULL;
    new_VC = (phylib_object *)malloc(sizeof(phylib_object));
    if (new_VC == NULL)
        return NULL;

    new_VC->type = PHYLIB_VCUSHION;
    new_VC->obj.vcushion.x = x;

    return new_VC;
}

phylib_table *phylib_new_table(void)
{
    phylib_table *new_tb = NULL;
    new_tb = (phylib_table *)malloc(sizeof(phylib_table));
    if (new_tb == NULL)
    {
        return NULL;
    }

    new_tb->time = 0.0;
    phylib_coord TOPR = {PHYLIB_TABLE_WIDTH, 0.0};
    phylib_coord BOTR = {PHYLIB_TABLE_WIDTH, PHYLIB_TABLE_LENGTH};
    phylib_coord MIDR = {PHYLIB_TABLE_WIDTH, (PHYLIB_TABLE_LENGTH * 0.5)};
    phylib_coord TOPL = {0.0, 0.0};
    phylib_coord BOTL = {0.0, PHYLIB_TABLE_LENGTH};
    phylib_coord MIDL = {0.0, (PHYLIB_TABLE_LENGTH * 0.5)};

    new_tb->object[0] = phylib_new_hcushion(0.0);
    new_tb->object[1] = phylib_new_hcushion(PHYLIB_TABLE_LENGTH);
    new_tb->object[2] = phylib_new_vcushion(0.0);
    new_tb->object[3] = phylib_new_vcushion(PHYLIB_TABLE_WIDTH);
    new_tb->object[4] = phylib_new_hole(&TOPL);
    new_tb->object[5] = phylib_new_hole(&MIDL);
    new_tb->object[6] = phylib_new_hole(&BOTL);
    new_tb->object[7] = phylib_new_hole(&TOPR);
    new_tb->object[8] = phylib_new_hole(&MIDR);
    new_tb->object[9] = phylib_new_hole(&BOTR);
    int i = 0;
    for (i = 10; i < PHYLIB_MAX_OBJECTS; i++)
    {
        new_tb->object[i] = NULL;
    }
    return new_tb;
}

void phylib_copy_object(phylib_object **dest, phylib_object **src)
{
    phylib_object *new_ob = NULL;
    new_ob = (phylib_object *)malloc(sizeof(phylib_object));
    if (*src == NULL)
    {
        *dest = NULL;
    }

    *dest = (phylib_object *)malloc(sizeof(phylib_object));
    memcpy(*dest, *src, sizeof(phylib_object));
    if (new_ob != NULL)
    {
        free(new_ob);
    }
}

phylib_table *phylib_copy_table(phylib_table *table)
{
    phylib_table *new_ctb = NULL;
    new_ctb = (phylib_table *)malloc(sizeof(phylib_table));
    if (new_ctb == NULL)
        return NULL;

    int i = 0;
    new_ctb->time = table->time;
    for (i = 0; i < PHYLIB_MAX_OBJECTS; i++)
    {
        if (table->object[i] != NULL)
        {
            phylib_copy_object(&new_ctb->object[i], &table->object[i]);
        }
        else
        {
            new_ctb->object[i] = NULL;
        }
    }

    return new_ctb; //*****
}

void phylib_add_object(phylib_table *table, phylib_object *object)
{
    int i = 0;
    for (i = 0; i < PHYLIB_MAX_OBJECTS; i++)
    {
        if (table->object[i] == NULL)
        {
            table->object[i] = object; //*******
            break;
        }
    }
}

void phylib_free_table(phylib_table *table)
{
    int i = 0;
    for (i = 0; i < PHYLIB_MAX_OBJECTS; i++)
    {
        if (table->object[i] != NULL)
        {
            free(table->object[i]);
        }
    }
    free(table);
}

phylib_coord phylib_sub(phylib_coord c1, phylib_coord c2)
{
    phylib_coord diff;

    diff.x = (c1.x - c2.x);
    diff.y = (c1.y - c2.y);

    return diff;
}
double phylib_square(double cx)
{
    return (cx * cx); // Square function for simplicity
}

double phylib_length(phylib_coord c)
{
    double b = phylib_square(c.x) + phylib_square(c.y); // pythagorean theorem
    return sqrt(b);
}

double phylib_dot_product(phylib_coord a, phylib_coord b)
{
    double dot = (a.x * b.x) + (a.y * b.y); // 
    return dot;
}

double phylib_distance(phylib_object *obj1, phylib_object *obj2)
{
    if (obj1->type != PHYLIB_ROLLING_BALL)
        return -1.0;
        
    if (obj2->type == 0)
    {
        double distx = phylib_square((obj2->obj.still_ball.pos.x - obj1->obj.rolling_ball.pos.x)); // x2 - x1 squared
        double disty = phylib_square((obj2->obj.still_ball.pos.y - obj1->obj.rolling_ball.pos.y)); // same for y//
        double distance = sqrt((distx + disty)); // square root of the sum, distance formula for coordinates
        return (distance - PHYLIB_BALL_DIAMETER); 
    }
    if (obj2->type == 1)
    {
        double distx = phylib_square((obj2->obj.rolling_ball.pos.x - obj1->obj.rolling_ball.pos.x));
        double disty = phylib_square((obj2->obj.rolling_ball.pos.y - obj1->obj.rolling_ball.pos.y)); // same as type 0 but with rolling ball
        double distance = sqrt((distx + disty));
        return (distance - PHYLIB_BALL_DIAMETER);
    }

    if (obj2->type == 2)
    {
        double distx = phylib_square((obj2->obj.hole.pos.x - obj1->obj.rolling_ball.pos.x)); // same as type 0 but using hole position
        double disty = phylib_square((obj2->obj.hole.pos.y - obj1->obj.rolling_ball.pos.y));
        double distance = sqrt((distx + disty));
        return (distance - PHYLIB_HOLE_RADIUS);
    }

    if (obj2->type == 3)
    {
        return fabs(obj2->obj.hcushion.y - obj1->obj.rolling_ball.pos.y) - PHYLIB_BALL_RADIUS; // only an y component so no square, it can be up or down so absolute value
    }

    if (obj2->type == 4)
    {
        return fabs(obj2->obj.vcushion.x - obj1->obj.rolling_ball.pos.x) - PHYLIB_BALL_RADIUS; // same as type 3 but with x
    }
    return -1.0;
}

double poseq(double pos, double vel, double accel, double time)
{
    double p = pos + vel * time + (accel * 0.5) * (time * time); // physics position equation p1 + v1*t + 1/2 a *t^2
    return p;
}
double veleq(double vel, double accel, double time)
{
    return (vel + accel * time); // physics velocity equation v1 + a1*t
}

void phylib_roll(phylib_object *new, phylib_object *old, double time)
{
    if ((old->type == PHYLIB_ROLLING_BALL) && (new->type == PHYLIB_ROLLING_BALL))
    {
        double posx = poseq(old->obj.rolling_ball.pos.x, old->obj.rolling_ball.vel.x, old->obj.rolling_ball.acc.x, time);
        double posy = poseq(old->obj.rolling_ball.pos.y, old->obj.rolling_ball.vel.y, old->obj.rolling_ball.acc.y, time); // set x and y from postion equations
        double velx = veleq(old->obj.rolling_ball.vel.x, old->obj.rolling_ball.acc.x, time); // set velocity x and y from velocity equation
        double vely = veleq(old->obj.rolling_ball.vel.y, old->obj.rolling_ball.acc.y, time);
        new->obj.rolling_ball.pos.x = posx; // position is always set no matter what
        new->obj.rolling_ball.pos.y = posy;
        if ((velx * old->obj.rolling_ball.vel.x < 0.0) && (vely * old->obj.rolling_ball.vel.y < 0.0)) // check if both x and y velocities changed signs
        {
            new->obj.rolling_ball.vel.x = 0.0;
            new->obj.rolling_ball.vel.y = 0.0;
            new->obj.rolling_ball.acc.x = 0.0;
            new->obj.rolling_ball.acc.y = 0.0;
        }
        else if ((velx * old->obj.rolling_ball.vel.x) < 0.0) // check if only x is changed
        {
            new->obj.rolling_ball.vel.x = 0.0;
            new->obj.rolling_ball.acc.x = 0.0;
        }
        else if ((vely * old->obj.rolling_ball.vel.y) < 0.0) // check if only y changed
        {
            new->obj.rolling_ball.vel.y = 0.0;
            new->obj.rolling_ball.acc.y = 0.0;
        }
        else
        {
            new->obj.rolling_ball.vel.x = velx;
            new->obj.rolling_ball.vel.y = vely;
        }
    }
}

unsigned char phylib_stopped(phylib_object *object)
{
    double speedin = phylib_length(object->obj.rolling_ball.vel);
    if (speedin < PHYLIB_VEL_EPSILON) /// less than phylib_Vel_Epsilon is out target for the ball stopping
    {   
        unsigned char numba =object->obj.rolling_ball.number;
        double xpos =object->obj.rolling_ball.pos.x;
        double ypos =object->obj.rolling_ball.pos.y;
        object->type = PHYLIB_STILL_BALL;
        object->obj.still_ball.number = numba;
        object->obj.still_ball.pos.x = xpos;  // Setting all the available attributes of still ball to the corresponding rolling ball attributes
        object->obj.still_ball.pos.y = ypos;
        object->obj.rolling_ball.vel.x = 0.0;
        object->obj.rolling_ball.vel.y = 0.0; // setting all attributes of rolling ball to 0 just for saftey sake
        object->obj.rolling_ball.acc.x = 0.0;
        object->obj.rolling_ball.acc.y = 0.0;
        return 1;
    }
    else
    {
        return 0;
    }
}

void phylib_bounce(phylib_object **a, phylib_object **b)
{

    if ((*a)->type != 1)     // checks if a is a ball, if not function does nothing
    {                   
        goto end; 
    }
    if ((*b) != NULL)
    {
        switch ((*b)->type)
        {
        case PHYLIB_HCUSHION:
            (*a)->obj.rolling_ball.vel.y *= -1.0;
            (*a)->obj.rolling_ball.acc.y *= -1.0; // ball hit a wall so it goes in the opposite direction
            break;
        case PHYLIB_VCUSHION:
            (*a)->obj.rolling_ball.vel.x *= -1.0;
            (*a)->obj.rolling_ball.acc.x *= -1.0;// ball hit a wall so it goes in the opposite direction
            break;

        case PHYLIB_HOLE:
            free((*a));
            (*a) = NULL; // ball entered a hole so it does not exist on the table;
            break;

        case PHYLIB_STILL_BALL:
            (*b)->type = PHYLIB_ROLLING_BALL;

            (*b)->obj.rolling_ball.acc.x = 0.0; // set everything of rolling ball to 0 for safety sake
            (*b)->obj.rolling_ball.acc.y = 0.0;
            (*b)->obj.rolling_ball.vel.x = 0.0;
            (*b)->obj.rolling_ball.vel.y = 0.0;
            (*b)->obj.rolling_ball.pos = (*b)->obj.still_ball.pos; // set corresponding values of rolling ball to still ball
            (*b)->obj.rolling_ball.number = (*b)->obj.still_ball.number;

        case PHYLIB_ROLLING_BALL:

            ;
            phylib_coord r_ab = phylib_sub((*a)->obj.rolling_ball.pos, (*b)->obj.rolling_ball.pos);

            phylib_coord v_rel = phylib_sub((*a)->obj.rolling_ball.vel, (*b)->obj.rolling_ball.vel);

            double nx = r_ab.x / phylib_length(r_ab);
            double ny = r_ab.y / phylib_length(r_ab);

            phylib_coord n;
            n.x = nx;
            n.y = ny;

            double v_rel_n = phylib_dot_product(v_rel, n);

            (*a)->obj.rolling_ball.vel.x = (*a)->obj.rolling_ball.vel.x - (v_rel_n * n.x);
            (*a)->obj.rolling_ball.vel.y = (*a)->obj.rolling_ball.vel.y - (v_rel_n * ny);

            (*b)->obj.rolling_ball.vel.x = (*b)->obj.rolling_ball.vel.x + (v_rel_n * nx);
            (*b)->obj.rolling_ball.vel.y = (*b)->obj.rolling_ball.vel.y + (v_rel_n * ny);

            double speeda = 0.0;
            double speedb = 0.0;
            speeda = phylib_length((*a)->obj.rolling_ball.vel);
            speedb = phylib_length((*b)->obj.rolling_ball.vel);
            if (speeda > PHYLIB_VEL_EPSILON)
            {
                (*a)->obj.rolling_ball.acc.x = (-(*a)->obj.rolling_ball.vel.x / speeda) * PHYLIB_DRAG;
                (*a)->obj.rolling_ball.acc.y = (-(*a)->obj.rolling_ball.vel.y / speeda) * PHYLIB_DRAG;
            }
            if (speedb > PHYLIB_VEL_EPSILON)
            {
                (*b)->obj.rolling_ball.acc.x = ((-(*b)->obj.rolling_ball.vel.x) / speedb) * PHYLIB_DRAG;
                (*b)->obj.rolling_ball.acc.y = ((-(*b)->obj.rolling_ball.vel.y) / speedb) * PHYLIB_DRAG;
            }
        end:
            break;
        }
    }
}

unsigned char phylib_rolling(phylib_table *t)
{
    unsigned char count = 0.0;
    int i = 9;
    for (i = 9; i < PHYLIB_MAX_OBJECTS; i++) // index starts at 9 because 10 and above will be where objects are placed
    {
        if (t->object[i] == NULL) // null check
            continue;

        else if (t->object[i]->type == PHYLIB_ROLLING_BALL) //counts if ball rolls
            count++;
    }
    return count;
}

phylib_table* phylib_segment(phylib_table* table) {
    if (table == NULL || !phylib_rolling(table)) {
        return NULL;  // Return NULL if no table or no rolling balls
    }

    double segtime = PHYLIB_SIM_RATE;
    phylib_table* CTable = phylib_copy_table(table);

    if (CTable != NULL) {
        int Eflag = 0;  // Loop exit flag, if 0 stay in loop, if 1 exit

        while (segtime < PHYLIB_MAX_TIME && !Eflag) {
            for (int i = 0; i < PHYLIB_MAX_OBJECTS; i++) { /// first loop to iterate up to maximum objects for the table
                if (CTable->object[i] != NULL && CTable->object[i]->type == 1) { // if the object is a rolling ball make it roll
                    phylib_roll(CTable->object[i], CTable->object[i], PHYLIB_SIM_RATE); // same object because one will be used to check as old while updating the ball

                    if (phylib_stopped(CTable->object[i])==1) { // check if stopping condition is met
                        Eflag = 1;  
                        break;  // Exit the inner loop
                    }

                    for (int j = 0; j < PHYLIB_MAX_OBJECTS; j++) { // SECOND LOOOP this loop's main purpose is to evaluate other objects while one object stays at rolling ball
                        if (CTable->object[j] != NULL && j != i) { // skips the rolling ball so it does not evaluate itself, and checks for NULL
                            if (phylib_distance(CTable->object[i], CTable->object[j]) < 0.0) { // if the distance between the rolling ball and an object is less than 0 they collided
                                phylib_bounce(&(CTable->object[i]), &(CTable->object[j])); // so bounce
                                Eflag = 1; 
                                break;  // Exit the inner loop
                            }
                        }
                    }
                }
            }

            segtime += PHYLIB_SIM_RATE;
        }
    }

    CTable->time += segtime;
    return CTable;
}

char *phylib_object_string(phylib_object *object)
{
    static char string[80];
    if (object == NULL)
    {
        snprintf(string, 80, "NULL;");
        return string;
    }
    switch (object->type)
    {
    case PHYLIB_STILL_BALL:
        snprintf(string, 80,
                 "STILL_BALL (%d,%6.1lf,%6.1lf)",
                 object->obj.still_ball.number,
                 object->obj.still_ball.pos.x,
                 object->obj.still_ball.pos.y);
        break;

    case PHYLIB_ROLLING_BALL:
        snprintf(string, 80,
                 "ROLLING_BALL (%d,%6.1lf,%6.1lf,%6.1lf,%6.1lf,%6.1lf,%6.1lf)",
                 object->obj.rolling_ball.number,
                 object->obj.rolling_ball.pos.x,
                 object->obj.rolling_ball.pos.y,
                 object->obj.rolling_ball.vel.x,
                 object->obj.rolling_ball.vel.y,
                 object->obj.rolling_ball.acc.x,
                 object->obj.rolling_ball.acc.y);
        break;

    case PHYLIB_HOLE:
        snprintf(string, 80,
                 "HOLE (%6.1lf,%6.1lf)",
                 object->obj.hole.pos.x,
                 object->obj.hole.pos.y);
        break;

    case PHYLIB_HCUSHION:
        snprintf(string, 80,
                 "HCUSHION (%6.1lf)",
                 object->obj.hcushion.y);
        break;

    case PHYLIB_VCUSHION:
        snprintf(string, 80,
                 "VCUSHION (%6.1lf)",
                 object->obj.vcushion.x);
        break;
        
    }
    return string;
}

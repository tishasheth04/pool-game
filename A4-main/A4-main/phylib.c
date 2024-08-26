#include "phylib.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>

/*
This function is a constructor for the new still ball. 
Firstly, it mallocs space for a phylib_object and if the malloc fails,
it instantly returns null. If the malloc does not fail,
it sets the type of the object to a phylib still ball, and sets the 
number, and position to the values in the parameters of the function.
Finally, it returns a still ball to where the function is being called.
*/

phylib_object *phylib_new_still_ball(unsigned char number, phylib_coord *pos){

  phylib_object * stillBall = NULL;
  //Mallocing space for the object with the size of the phylib object.
  stillBall = malloc(sizeof(phylib_object));

  //Harness if the mallocing space fails.
  if(stillBall == NULL){
    return NULL;
  }

  //Sets the appropriate values for the specific type of object.
  stillBall->type = PHYLIB_STILL_BALL;

  stillBall->obj.still_ball.number = number;
  stillBall->obj.still_ball.pos.x =pos->x;
  stillBall->obj.still_ball.pos.y =pos->y;

  return stillBall;

}

/*
This is similar to the first function, however the same process is being applied 
to a rolling ball object instead of a still ball. It first mallocs space for
the object of size phylib_object then if the mallocing fails, NULL is returned back to the calling program.
Else, the values in the parameters are stored in the appropriate areas.
Finally, the object is returned back to the calling program.
*/

phylib_object *phylib_new_rolling_ball(unsigned char number, phylib_coord *pos, phylib_coord *vel, phylib_coord *acc){

  phylib_object * rollingBall = NULL;
  //Mallocing space for the object
  rollingBall = malloc(sizeof(phylib_object));

  //This code is in case the mallocing fails.
  if(rollingBall == NULL){
    return NULL;
  }

  //Values are being stored based on what is being sent into the function.

  rollingBall->type = PHYLIB_ROLLING_BALL;
  rollingBall->obj.rolling_ball.number = number;
  rollingBall->obj.rolling_ball.pos.x = pos->x;
  rollingBall->obj.rolling_ball.pos.y = pos->y;
  rollingBall->obj.rolling_ball.vel.x = vel->x;
  rollingBall->obj.rolling_ball.vel.y = vel->y;
  rollingBall->obj.rolling_ball.acc.x = acc->x;
  rollingBall->obj.rolling_ball.acc.y = acc->y;

  return rollingBall;
}

/*
This function is a constructor for a new hole. The main premise of this
function is to create a new hole. First, it mallocs space for a phylib_object,
if the mallocing fails, NULL is returned back to the calling program.
Else, the values that are being passed as arguments will be stored in the structure of a hole.
Finally, a hole object is returned to the calling program.
*/

phylib_object *phylib_new_hole(phylib_coord *pos){

  phylib_object * hole = NULL;
  //Mallocing space for the object.
  hole = malloc(sizeof(phylib_object));

  //In case mallocing fails, NULL value is returned.
  if(hole == NULL){
    return NULL;
  }

  //Values are being set in the structure based on the values in the parameters.
  hole->type = PHYLIB_HOLE;
  hole->obj.hole.pos.x = pos->x;
  hole->obj.hole.pos.y = pos->y;

  return hole;

}

/*
This function is responsible for creating a new h cushion object.
First it mallocs space for the phylib_object. Next, it checks to 
see if the malloc was a success, if not, it returns NULL back to the calling program.
Else, it sets the values for a new h cushion in the structure.
Finally, it returns the new hCushion object to the calling program.
*/

phylib_object *phylib_new_hcushion(double y){

  phylib_object * hCushion = NULL;
  //Mallocing space for the object
  hCushion = malloc(sizeof(phylib_object));

  //Checking to see if mallocing was successful
  if(hCushion == NULL){
    return NULL;
  }

  //Setting the values with the values in the parameters and returning the object
  hCushion->type = PHYLIB_HCUSHION;
  hCushion->obj.hcushion.y = y;

  return hCushion;
}

/*
This function creates a new v cushion object. 
First, it mallocs space for the new object. If the mallocing
fails however, it returns NULL back to the calling program.
Else, it sets the values in the structure to the values
being sent in the parameters. Finally, it returns the
new v cushion object to the calling program.
*/

phylib_object *phylib_new_vcushion(double x){

  phylib_object * vCushion = NULL;
  //Mallocing space for the function
  vCushion = malloc(sizeof(phylib_object));

  //Returns null if mallocing fails
  if(vCushion == NULL){
    return NULL;
  }
  //Sets the values in the function and returns it
  vCushion->type = PHYLIB_VCUSHION;
  vCushion->obj.vcushion.x = x;

  return vCushion;

}

/*
This function creates a new table for the game.
First, it mallocs space for the table using the size of a phylib_table.
If the mallocing fails, NULL is sent back to the calling program indicating that mallocing was not successful
It creates 6 different positions for the 6 holes on a pool table.
Their coordinates are based on the location at which these holes will reside.
Next, 0-9 values are added to the array of a table including the cushions, 
holes. The remaining object are all set to null as they can be different types of balls.
Finally, a new table object is returned back to the calling program.
*/

phylib_table *phylib_new_table(void){

  phylib_table * table = NULL;
  //Mallocing space for the table
  table = malloc(sizeof(phylib_table));

  //If the mallocing fails, NULL is returned
  if(table == NULL){
    return NULL;

  }

  //Different positions for the holes.
    //most left top
  phylib_coord pos;
  pos.x = 0;
  pos.y = 0;

  phylib_coord hMaxPos;
  hMaxPos.x = PHYLIB_TABLE_WIDTH;
  hMaxPos.y = 0;

  phylib_coord vMaxPos;
  vMaxPos.x = 0;
  vMaxPos.y = PHYLIB_TABLE_LENGTH;

  //bottom right
  phylib_coord maxPos;
  maxPos.x = PHYLIB_TABLE_WIDTH;
  maxPos.y = PHYLIB_TABLE_LENGTH;

  phylib_coord vHalfPos;
  vHalfPos.x = 0;
  vHalfPos.y = (PHYLIB_TABLE_LENGTH / 2);

  phylib_coord hHalfPos;
  hHalfPos.x = PHYLIB_TABLE_WIDTH;
  hHalfPos.y = (PHYLIB_TABLE_LENGTH / 2);

  //Adding specific objects to the array and setting the time of the table to 0.0
  table->time = 0.0;
  table->object[0] = phylib_new_hcushion(0.0);
  table->object[1] = phylib_new_hcushion(PHYLIB_TABLE_LENGTH);
  table->object[2] = phylib_new_vcushion(0.0);
  table->object[3] = phylib_new_vcushion(PHYLIB_TABLE_WIDTH);
  table->object[4] = phylib_new_hole(&pos);
  table->object[5] = phylib_new_hole(&vHalfPos);
  //table->object[5] = phylib_new_hole(&hMaxPos);
  table->object[6] = phylib_new_hole(&vMaxPos);
  table->object[7] = phylib_new_hole(&hMaxPos); 
  //table->object[7] = phylib_new_hole(&maxPos);  
  //table->object[8] = phylib_new_hole(&vHalfPos);
  table->object[8] = phylib_new_hole(&hHalfPos);
  table->object[9] = phylib_new_hole(&maxPos);

  //Setting the remaining values to null and returning the object back to the calling program
  for(int i = 10; i < PHYLIB_MAX_OBJECTS; i++){
    table->object[i] = NULL;
  }

  return table;

}

/*
The main premise of this function is to copy a object that is present in the table.
For this, I first check to see if the original object being sent as a argument is null or not.
If it is not null, I make a new object called newObject and malloc space for it.
I make *dest = to the newObject I have created and call memcpy so everything is copied into the new *dest
from the source. If *src is null, I make *dest = null as well. As this function works with pointers,
nothing will be returned back to the calling program.
*/

void phylib_copy_object(phylib_object **dest, phylib_object **src){

  //Only executes if the src object is not null
  if(*src != NULL){
    phylib_object * newObject = malloc(sizeof(phylib_object));
    *dest = newObject;
    memcpy(*dest,*src, sizeof(phylib_object));

  }
  else{
    *dest = NULL;
  }

}

/*
This function is responsible for creating a copy of the orignal table.
Firstly, if the table that is being passed a parameter to the function is null, the value
NULL is returned to the calling program. Else, I create a new table object by mallocing space for this new table.
Else, I make sure to make all objects in the new table object I created NULL. I do this because if I dont, there is 
conditional jumps that occur when running with valgrind. Next, I go through another for loop that runs till
the max objects and checks if the orignal tbale at that index had a object or if it was null. If it is not null at that
index, then the new table at index i copies the object of table at index i using the copy object function.
Once the for loop ends, the new table time is set to the same time the table object time was set to. 
Finally, the new table object is sent back to the calling program.
*/

phylib_table *phylib_copy_table(phylib_table * table){

  //Checks if the table that is sent into the function is null. If it is, null is sent to the calling program.
  if(table == NULL){
    return NULL;
  }

  //Mallocing space for a new table object
  phylib_table * newTable = malloc(sizeof(phylib_table));

  //In case malloc fails
  if(newTable == NULL){
    return NULL;
  }

  //Setting all objects in the new table to null to avoid conditional jumps and other issues.
  for(int i = 0; i < PHYLIB_MAX_OBJECTS; i++){
    newTable->object[i] = NULL;
  }

  //This for loop copies each object from the table (from parameter) to the new table object I created by calling copy_object
  //for each iteration.
  for(int i = 0; i < PHYLIB_MAX_OBJECTS; i++){
    if(table->object[i] != NULL){
      phylib_copy_object(&newTable->object[i],&table->object[i]);
    }
  }

  //Time is being set as well and the new table is returned to the calling program.
  newTable->time = table->time;

  return newTable;
}


/*
The main premise is to add a new object to the table. The object that is to be added into the table is being sent in as a parameter.
To achieve this, I first create a while loop that runs as long as the object in the table is not null and does not exceed the max object limit.
Once a object is null, that index is used to add the new object to the table. First however, it is checked to see if 
the object at that index is in fact null and the index is less than the max. If so, the new object is added to the table.
*/

void phylib_add_object(phylib_table *table, phylib_object *object){

  int t = 0;

  //Loop runs till a object is null or if the max limit of objects is reached
  while(table->object[t] != NULL && t < PHYLIB_MAX_OBJECTS){
    t++;
  }

  //If object at that index is null and the index is less than max objects, the object is added to the table.
  if(table->object[t] == NULL && t < PHYLIB_MAX_OBJECTS){
     table->object[t] = object;
  }

}


/*
The main premise of this function to free all the objects in the table and then free the table at the end.
To achieve this, I create a for loop that runs till the max number of objects that can fit into the table.
In the loop, I have a if statement that checks if the object at that index in the table is null.
If it is not null, then the object is freed. I do this check because if the object at that index is already null,
there is nothing to free in the first place. Once the for loop ends, I free the table itself.
*/

void phylib_free_table(phylib_table * table){

  //Frees each object in the table
  for(int i = 0; i < PHYLIB_MAX_OBJECTS; i++){
     if(table->object[i] != NULL){
       free(table->object[i]);
    }
  }

  //Frees the table
  free(table);

}

/*
The main premise of this function is to find the difference between
to positions. To achieve this, I create a phylib_coord structure.
Then, for both x and y, I subtract the first structure value being passed as a parameter with the second value.
Finally, I return the structure back to the calling program.
*/

phylib_coord phylib_sub(phylib_coord c1, phylib_coord c2){

  phylib_coord pos;

  //Subtracting the values and storing them in the new structure I created.
  pos.x = c1.x-c2.x;
  pos.y = c1.y-c2.y;

  return pos;

}

/*
For this function I am supposed to find the length of the vector.
To calculate this length, I use the pythagorean's theorem. First, I created multiple variables.
I have multiplied c.x with itself and c.y with itself to square both those values.
I have stored both those values into the appropriate variables.
Then, I added both those values and stored it into the total variable.
Next, I squarerooted the total value and stored it into a variable called vector and returning it to the calling program.
*/

double phylib_length(phylib_coord c){

  double vector = 0;
  double xTotal =0;
  double yTotal = 0;
  double total = 0;

  //Squaring the coordinates
  xTotal = c.x * c.x;
  yTotal = c.y * c.y;
  
  //Adding them and square rooting it 
  total = xTotal + yTotal;
  vector = sqrt(total);

  return vector;
}

/*
This function calculates the dot product between two vectors.
To achieve this, I multiply the x values and the y values
and I add them together. I store that added value into a variable called total.
Finally, I return total.
*/

double phylib_dot_product(phylib_coord a, phylib_coord b){

  double xTotal = 0;
  double yTotal = 0;
  double total = 0;

  xTotal = a.x * b.x;
  yTotal = a.y * b.y;
  total = xTotal + yTotal;

  return total;
}

/*
The main premise of this function is to calculate the distance between two objects.
First, I check if the first object is a rolling ball. If not I return -1.0
Next, I have a couple of if statements to check what the type of the second object is.
Depending on the second object type, that block of code runs. For each case, there is a specific operation that is done to
get the desired value. In each block of code, that value is returned.
If none of the cases match, -1.0 is returned back to the calling program indicating that something is wrong.

*/

double phylib_distance(phylib_object *obj1, phylib_object *obj2){

  phylib_coord sub;
  double length = 0;
  double ballDistance = 0;
  double holeDistance = 0;
  double hCushionDistance = 0;
  double vCushionDistance = 0;

  //In case the first object is not a rolling ball
  if(obj1->type != PHYLIB_ROLLING_BALL){
    return -1.0;

  }
  //If the second object is a rolling ball
  if(obj2->type == PHYLIB_ROLLING_BALL){
    sub = phylib_sub(obj2->obj.rolling_ball.pos, obj1->obj.rolling_ball.pos);
    length = phylib_length(sub);
    ballDistance = length - PHYLIB_BALL_DIAMETER;
    return ballDistance;
  }
  //If the second object is a still ball
  if(obj2->type == PHYLIB_STILL_BALL){
    sub = phylib_sub(obj2->obj.still_ball.pos, obj1->obj.still_ball.pos);
    length=phylib_length(sub);
    ballDistance = length - PHYLIB_BALL_DIAMETER;
    return ballDistance;
  }
  //If the second object is a hole
  if(obj2->type == PHYLIB_HOLE){
    sub = phylib_sub(obj2->obj.hole.pos, obj1->obj.rolling_ball.pos);
    length = phylib_length(sub);
    holeDistance = length - PHYLIB_HOLE_RADIUS;
    return holeDistance;
  }
  //If the second object is a horizontal cushion
  if(obj2->type == PHYLIB_HCUSHION){
   length = obj2->obj.hcushion.y - obj1->obj.rolling_ball.pos.y;
   hCushionDistance = (fabs(length)) - PHYLIB_BALL_RADIUS;
   return hCushionDistance;

  }
  //If the second object is a vertical cushion
  if(obj2->type == PHYLIB_VCUSHION){
   length = obj2->obj.vcushion.x - obj1->obj.rolling_ball.pos.x;
   vCushionDistance = (fabs(length)) - PHYLIB_BALL_RADIUS;
   return vCushionDistance;
  }
  //If none of the cases are met
  return -1.0;


}

/*
The main premise of this function is to actually showcase what occured with the ball.
Essentially, it updates a new phylib object that represents a old phylib object after it has rolled. It also has to make sure
that both the new and old objects are rolling balls.
Therefore, I have a if statement that checks to see if they both are rolling balls,.
If so, the values are updated for the new rolling ball object.
In this if statement, it also checks if the velocity changes sign at any moment.
If so, it updates the velocity and acceleration to 0 for x and/or y.
*/

void phylib_roll(phylib_object *new, phylib_object *old, double time){

  if(new->type == PHYLIB_ROLLING_BALL && old->type == PHYLIB_ROLLING_BALL){
    new->obj.rolling_ball.pos.x = old->obj.rolling_ball.pos.x + ((old->obj.rolling_ball.vel.x) * (time)) + ((0.5 * old->obj.rolling_ball.acc.x) * (time * time));
    new->obj.rolling_ball.pos.y = old->obj.rolling_ball.pos.y + ((old->obj.rolling_ball.vel.y) * (time)) + ((0.5 * old->obj.rolling_ball.acc.y) * (time * time));
    new->obj.rolling_ball.vel.x = old->obj.rolling_ball.vel.x + ((old->obj.rolling_ball.acc.x) * (time));
    new->obj.rolling_ball.vel.y = old->obj.rolling_ball.vel.y + ((old->obj.rolling_ball.acc.y) * (time));
    
    if(new->obj.rolling_ball.vel.x * (old->obj.rolling_ball.vel.x) < 0){
      new->obj.rolling_ball.vel.x = 0;
      new->obj.rolling_ball.acc.x = 0;
    }

    if(new->obj.rolling_ball.vel.y * (old->obj.rolling_ball.vel.y) < 0){
       new->obj.rolling_ball.vel.x = 0;
       new->obj.rolling_ball.acc.y = 0;
    }

  }

}

/*
This function checks to see if a rolling ball has stopped.
To achieve this, I have created multiple variables that will support me in achieving the premise of this function.
First, I call the length function to find the speed of the ball.
If the returned value (speed) is less than the constant vel epsilon then I change the type of the ball to a still ball and
move the values over to the new structure. Since the type changed
from rolling ball to still ball, I return 1. If the speed is not less than the constant vel epsilon
I return 0.


*/

unsigned char phylib_stopped(phylib_object *object){

  double speed = 0;
  unsigned char number = object->obj.rolling_ball.number;
  phylib_coord oldPos;
  oldPos.x = object->obj.rolling_ball.pos.x;
  oldPos.y = object->obj.rolling_ball.pos.y;
  phylib_coord pos;
  pos.x = object->obj.rolling_ball.vel.x;
  pos.y = object->obj.rolling_ball.vel.y;

  speed = phylib_length(pos);

  if(speed < PHYLIB_VEL_EPSILON){
    object->type = PHYLIB_STILL_BALL;
    object->obj.still_ball.number = number;
    object->obj.still_ball.pos.x = oldPos.x;
    object->obj.still_ball.pos.y = oldPos.y;
    return 1;

  }

  return 0;

}


/*
This function checks the second object that is passed as a parameter 
and based on the type, specific blocks of code are executed.
One thing to add is that after the still ball case there is no break statement
as in the still ball block of code, it changes the type of the second object to a rolling ball.
Since there is no break statement, the next block of code is executed regardless.
*/

void phylib_bounce(phylib_object **a, phylib_object **b){

  double negative = -1;
  double length = 0;
  unsigned char number; //= (*b)->obj.still_ball.number;
  phylib_coord pos;
  phylib_coord r_ab;
  phylib_coord v_rel;
  double v_rel_n;
  double speedA;
  double speedB;
  phylib_coord n;
  //pos.x =  (*b)->obj.still_ball.pos.x;
  //pos.y =  (*b)->obj.still_ball.pos.y;
  
  switch((*b)->type){

    case (PHYLIB_HCUSHION):
      (*a)->obj.rolling_ball.vel.y = ((*a)->obj.rolling_ball.vel.y * negative);
      (*a)->obj.rolling_ball.acc.y = ((*a)->obj.rolling_ball.acc.y * negative);
      break;
    case (PHYLIB_VCUSHION):
      (*a)->obj.rolling_ball.vel.x = ((*a)->obj.rolling_ball.vel.x * negative);
      (*a)->obj.rolling_ball.acc.x = ((*a)->obj.rolling_ball.acc.x * negative);
      break;
    case (PHYLIB_HOLE):
      free((*a));
      (*a) = NULL;
      break;
    case (PHYLIB_STILL_BALL):
      number = (*b)->obj.still_ball.number;
      pos.x =  (*b)->obj.still_ball.pos.x;
      pos.y =  (*b)->obj.still_ball.pos.y;
      (*b)->type = PHYLIB_ROLLING_BALL;
      (*b)->obj.rolling_ball.number = number;
      (*b)->obj.rolling_ball.pos.x = pos.x;
      (*b)->obj.rolling_ball.pos.y = pos.y;
      (*b)->obj.rolling_ball.vel.x = 0.0;
      (*b)->obj.rolling_ball.vel.y = 0.0;
      (*b)->obj.rolling_ball.acc.x = 0.0;
      (*b)->obj.rolling_ball.acc.y = 0.0;

    case (PHYLIB_ROLLING_BALL):
      r_ab = phylib_sub((*a)->obj.rolling_ball.pos, (*b)->obj.rolling_ball.pos);
      v_rel = phylib_sub((*a)->obj.rolling_ball.vel, (*b)->obj.rolling_ball.vel);
      length = phylib_length(r_ab);
      n.x = (r_ab.x / length);
      n.y = (r_ab.y / length);
      v_rel_n = phylib_dot_product(v_rel, n);
      (*a)->obj.rolling_ball.vel.x =  (*a)->obj.rolling_ball.vel.x - (v_rel_n *  n.x);
      (*a)->obj.rolling_ball.vel.y =  (*a)->obj.rolling_ball.vel.y - (v_rel_n *  n.y);
      (*b)->obj.rolling_ball.vel.x =  (*b)->obj.rolling_ball.vel.x + (v_rel_n *  n.x);
      (*b)->obj.rolling_ball.vel.y =  (*b)->obj.rolling_ball.vel.y + (v_rel_n *  n.y);
      speedA = phylib_length((*a)->obj.rolling_ball.vel);
      speedB = phylib_length((*b)->obj.rolling_ball.vel);
    
      if(speedA > PHYLIB_VEL_EPSILON){
        (*a)->obj.rolling_ball.acc.x = (-1)*((*a)->obj.rolling_ball.vel.x)/ (speedA) * PHYLIB_DRAG;
        (*a)->obj.rolling_ball.acc.y = (-1)*((*a)->obj.rolling_ball.vel.y)/ (speedA) * PHYLIB_DRAG;
      }

      if(speedB > PHYLIB_VEL_EPSILON){
        (*b)->obj.rolling_ball.acc.x = (-1)*(((*b)->obj.rolling_ball.vel.x)/ (speedB) * PHYLIB_DRAG);
        (*b)->obj.rolling_ball.acc.y = (-1)*(((*b)->obj.rolling_ball.vel.y)/ (speedB) * PHYLIB_DRAG);

      }
      break;

     //n = 

  }

}

/*
The main purpose of this function is to check how many rolling balls there are in the table.
For this, I am iterating through a for loop and if the object at that index is not null AND the type of the object is of rolling ball
I increment the variable check.
At the end, I return check.
*/

unsigned char phylib_rolling(phylib_table *t){

  unsigned char check = 0;

  //if(t == NULL){
    //return -1;
  //}
 
  for(int i = 0; i < PHYLIB_MAX_OBJECTS; i++){
    if(t->object[i] != NULL && (t->object[i]->type == PHYLIB_ROLLING_BALL)){
      check++;
    }

  }
  return check;
}

/*
This function showcases a segment of how the ball moves.
First, I call the rolling function sending the table as a arguement.
If the number of rolling balls is 0 or less, it returns NULL.
Next, I call copy table function and store the returned table into a object called copiedTable.
I have a while loop running that runs till time hits the MAX_TIME.
Inside that while loop, I have a for loop running until the MAX_OBJECTS.
If certain conditions are met inside that for loop, I call the roll function.
Inside the while loop, I have another for loop that runs till teh MAX_OBJECTS. Inside the for loop, I have another if statement and if those conditions are met,
I another set of a for loop that have nested if statements and they call bounce to check the distance of a particular 
object with other objects on the table if the distance between those two objects is less than 0.0.
Then, the time is incremeted and the new copied table is returned back to the calling program.
Finally, I have another for loop that runs till the MAX_OBJECTS and in that I have another if statement. IF the conditions are met,
the rolling function is called and if 1 is returned by rolling, we return a copied table to the calling program.
At the end the copied table is sent back to the calling program.
*/

phylib_table *phylib_segment(phylib_table *table){

  if(table == NULL){
    return NULL;
  }

  unsigned char numberOfRollingBalls = phylib_rolling(table);
  unsigned char rollingCheck = 0;
  double time = PHYLIB_SIM_RATE;
  double distance = 0;


  if(numberOfRollingBalls <= 0){
    return NULL;

  }

  phylib_table * copiedTable = phylib_copy_table(table);


  while(time < PHYLIB_MAX_TIME){

    for(int i = 0; i < PHYLIB_MAX_OBJECTS; i++){
      if((copiedTable->object[i] != NULL)  && (copiedTable->object[i]->type == PHYLIB_ROLLING_BALL)){
        phylib_roll(copiedTable->object[i], table->object[i], time);
      } // end of if calling roll

    } //end of for 


    for(int j = 0; j < PHYLIB_MAX_OBJECTS; j++){
      if((copiedTable->object[j] != NULL) && (copiedTable->object[j]->type == PHYLIB_ROLLING_BALL)){

      	for(int k = 0; k < PHYLIB_MAX_OBJECTS; k++){
          if(copiedTable->object[k] != NULL && (j != k)){
            distance = phylib_distance(copiedTable->object[j], copiedTable->object[k]);
            if(distance < 0.0){
              phylib_bounce(&(copiedTable->object[j]), &(copiedTable->object[k]));
              copiedTable->time += time;
              return copiedTable;
            } //nested if
          } //outside if
        } //nested for
      }
    }// outside for

    for(int l = 0; l <PHYLIB_MAX_OBJECTS ; l++){
      if(copiedTable->object[l] != NULL && (copiedTable->object[l]->type == PHYLIB_ROLLING_BALL)){
        rollingCheck = phylib_stopped(copiedTable->object[l]);
        if(rollingCheck == 1){
          copiedTable->time += time;
          return copiedTable;
        } //if statement
      }//outside if 
    } //for statement



    time = time + PHYLIB_SIM_RATE;
  }
  copiedTable->time += time;
  return copiedTable;
}




char *phylib_object_string( phylib_object *object )
{
static char string[80];
if (object==NULL)
{
snprintf( string, 80, "NULL;" );
return string;
}
switch (object->type)
{
case PHYLIB_STILL_BALL:
snprintf( string, 80,
"STILL_BALL (%d,%6.1lf,%6.1lf)",
object->obj.still_ball.number,
object->obj.still_ball.pos.x,
object->obj.still_ball.pos.y );
break;
case PHYLIB_ROLLING_BALL:
snprintf( string, 80,
"ROLLING_BALL (%d,%6.1lf,%6.1lf,%6.1lf,%6.1lf,%6.1lf,%6.1lf)",
object->obj.rolling_ball.number,
object->obj.rolling_ball.pos.x,
object->obj.rolling_ball.pos.y,
object->obj.rolling_ball.vel.x,
object->obj.rolling_ball.vel.y,
object->obj.rolling_ball.acc.x,
object->obj.rolling_ball.acc.y );
break;
case PHYLIB_HOLE:
snprintf( string, 80,
"HOLE (%6.1lf,%6.1lf)",
object->obj.hole.pos.x,
object->obj.hole.pos.y );
break;
case PHYLIB_HCUSHION:
snprintf( string, 80,
"HCUSHION (%6.1lf)",
object->obj.hcushion.y );
break;
case PHYLIB_VCUSHION:
snprintf( string, 80,
"VCUSHION (%6.1lf)",
object->obj.vcushion.x );
break;
}
return string;
}

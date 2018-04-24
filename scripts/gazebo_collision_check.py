#! /usr/bin/env python
from gazebo_msgs.srv import GetModelState
import rospy
import math
import sys
argvs = sys.argv
if len(argvs) != 2:
    print ("usage: rosrun gazebo_collision_check gazebo_collision_check <output_filename.csv>")
    exit()

class Actor:
    min_dist = 100.0
    def __init__(self, name, relative_entity_name):
        self._name = name
        self._relative_entity_name = relative_entity_name

class CollisionCheck:

    _actorListDict = {
        'actor0': Actor('actor0', 'cog'),
        'actor1': Actor('actor1', 'cog'),
        'actor2': Actor('actor2', 'cog'),
        'actor3': Actor('actor3', 'cog'),
        'actor4': Actor('actor4', 'cog'),
        'actor5': Actor('actor5', 'cog'),
        'actor6': Actor('actor6', 'cog'),
        'actor7': Actor('actor7', 'cog'),
        'actor8': Actor('actor8', 'cog'),
        'actor9': Actor('actor9', 'cog'),
    }

    collision_count = 0
    def show_gazebo_models(self):
        try:
            model_coordinates = rospy.ServiceProxy('/gazebo/get_model_state', GetModelState)
            for actor in self._actorListDict.itervalues():
                actorName = str(actor._name)
                resp_coordinates = model_coordinates(actorName, actor._relative_entity_name)

                position = [resp_coordinates.pose.position.x, resp_coordinates.pose.position.y]
                tmp_dist = math.sqrt(position[0] * position[0] + position[1] * position[1])

                if actor.min_dist > tmp_dist:
                    actor.min_dist = tmp_dist
                print (actorName)
                print ("min_dist:" + str(actor.min_dist))
                print


        except rospy.ServiceException as e:
            rospy.loginfo("Get Model State service call failed:  {0}".format(e))

    def save_result(self):
        f = open(argvs[1], 'w')
        for actor in self._actorListDict.itervalues():
            result = str(actor._name) + "," + str(actor.min_dist) + "\n"
            f.write(result)
        f.close()


if __name__ == '__main__':
    rospy.init_node('gazebo_collision_check')
    cc = CollisionCheck()
    # rospy.spin()
    r = rospy.Rate(10)
    try:
        while not rospy.is_shutdown():
            cc.show_gazebo_models()
            r.sleep()
    except rospy.ROSInterruptException:
        cc.save_result()
        print ("Save Result")

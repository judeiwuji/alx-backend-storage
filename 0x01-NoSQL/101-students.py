#!/usr/bin/env python3
"""Top students"""


def top_students(mongo_collection):
    """function that returns all students sorted
    by average score

    Args:
        mongo_collection(Collection)
    """
    return mongo_collection.aggregate(
        [{"$project": {"_id": "$_id", "name": 1,
                       "averageScore": {"$avg": "$topics.score"}},
          },
         {"$sort": {"averageScore": -1}}
         ])

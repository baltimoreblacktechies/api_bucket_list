"""
This is the bucket_list module and supports all the ReST actions for the
bucket list collection
"""

# 3rd party modules
from flask import make_response, abort
from config import db
from models import BucketListItem, BucketListItemSchema


def get_bucket_list():
    """
    This function responds to a request for /api/bucketList
    with the complete lists of bucket list items

    :return:        json string of list of bucket list items
    """
    # Get the list of bucket list items from the database
    bucketList = BucketListItem.query.order_by(BucketListItem.item_id).all()

    print('bucketlist: ', bucketList)
    # Serialize the data for the response
    if not bucketList:
        return 'No data', 200

    schema = BucketListItemSchema(many=True)
    data = schema.dump(bucketList)
    return data


def get_bucket_list_item(item_id):
    """
    This function responds to a request for /api/bucketList/{id}
    with item from databse with matching id

    :param id:      id of item to find
    :return:        item matching id
    """

    print('gets here')
    print(type(item_id))

    item = BucketListItem.query.get(item_id)

    if item is not None:
        schema = BucketListItemSchema()
        data = schema.dump(item)
        return data
    else:
        abort(404, f"BucketListItem with {item_id} not found.")


def create_bucket_list_item(item):
    """
    This function creates a new bucket list item in the database
    based on the passed in item data

    :param item:    item to create in database
    :return:        201 on success, 406 on item exists
    """
    # if there is no id we can assume we are creating
    if 'item_id' not in item:

        title = item.get('title')

        # We don't allow duplicate titles so check that one doesn't exist
        existing_item = (
            BucketListItem.query.filter(BucketListItem.title == title)
            .one_or_none()
        )

        # Can we insert this item?
        if existing_item is None:
            # Create BucketListItem instance using schema and the passed item
            schema = BucketListItemSchema()
            new_item = schema.load(item, session=db.session)

            # Add the item to the database
            db.session.add(new_item)
            db.session.commit()

            # Serialize and return the newly created item in response
            data = schema.dump(new_item)

            return data, 201

        # Duplicate title found so throw helpful error
        else:
            abort(406, f"BucketListItem with title {title} already exists")

    # Duplicate id found so throw helpful error
    else:
        abort(406, f"BucketListItem {item.get('item_id')} already exists")


def update_bucket_list_item(item_id, item):
    """
    This function updates an existing item in the database
    Throws an error if an item with the same title as what we want to
    update to already exists in the database.

    :param item_id:     Id of the bucket list item to update in the db
    :param item:        item to update
    :return:             updated bucket list item structure
    """
    # Get the person requested from the db into session
    update_item = BucketListItem.query.filter(
        BucketListItem.item_id == item_id
    ).one_or_none()

    title = item.get('title')

    # If the item we are trying to update doesn't exist return an error
    if update_item is None:
        abort(404, f"BucketListItem not found for Id: {item_id}")

    # Try to find an existing item with the same title as the update
    existing_item = (
        BucketListItem.query.filter(BucketListItem.title == title)
        .one_or_none()
    )

    # If creating an item that duplicates an existing item title throw error
    if existing_item is not None and existing_item.item_id != item_id:
        abort(
            409,
            f"Duplicate: BucketListItem with title {title} exists already")

    # Safe to update!
    else:

        # turn the passed item into a db object
        schema = BucketListItemSchema()
        update = schema.load(item, session=db.session)

        # merge the new object into the old and commit it to the db
        db.session.merge(update)
        db.session.commit()

        # reload item to get new timestamp
        reloaded_item = BucketListItem.query.get(item_id)

        data = schema.dump(reloaded_item, session=db.session)

        return data, 200


def delete_bucket_list_item(item_id):
    """
    This function deletes a bucket list item from the database

    :param item_id:     Id of the item to delete
    :return:            200 on successful delete, 404 if not found
    """
    # Get the person requested
    item = BucketListItem.query.filter(
        BucketListItem.item_id == item_id).one_or_none()

    # Did we find a person?
    if item is not None:
        db.session.delete(item)
        db.session.commit()
        return make_response(f"Person {item_id} deleted", 200)

    # If failed to find item, return an error
    else:
        abort(404, f"Person not found for Id: {item_id}")

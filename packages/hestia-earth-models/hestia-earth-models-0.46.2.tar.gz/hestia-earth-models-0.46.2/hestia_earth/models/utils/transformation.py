def previous_transformation(cycle: dict, transformations: list, transformation: dict):
    tr_id = transformation.get('previousTransformationId')
    return next(
        (v for v in transformations if v.get('transformationId') == tr_id),
        cycle
    )

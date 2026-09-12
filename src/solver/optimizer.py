def choose_best(
    candidates,
    simulator,
    scorer
):

    best_actions = None

    best_score = float(
        "-inf"
    )

    for actions in candidates:

        state = simulator.run(
            actions
        )

        score = scorer(
            state
        )

        if score > best_score:

            best_score = score

            best_actions = actions

    return (
        best_actions or [],
        best_score
    )
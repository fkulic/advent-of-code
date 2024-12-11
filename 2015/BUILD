[
    cc_binary(
        name = day.replace(".cpp", ""),
        srcs = [day],
    )
    for day in glob(["day*.cpp"])
]

[
    py_binary(
        name = day.replace(".py", ""),
        srcs = [day],
        python_version = "PY3",
    )
    for day in glob(["day*.py"])
]

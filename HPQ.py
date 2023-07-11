fibo_type = [
    0.236,
    0.276,
    0.382,
    0.447,
    0.5,
    0.618,
    0.707,
    0.786,
    0.886,
    1.0,
    1.128,
    1.272,
    1.414,
    1.618,
    2.0,
    2.236,
    2.618,
    3.618,
]

XABCD_patterns = [
    {
        "pattern": "ideal gartley",
        "minXB": 0.618,
        "maxXB": 0.618,
        "minAC": 0.618,
        "maxAC": 0.786,
        "minBD": 1.272,
        "maxBD": 1.618,
        "minXD": "-",
        "maxXD": "-",
    },
    {
        "pattern": "618 gartley",
        "minXB": 0.618,
        "maxXB": 0.618,
        "minAC": 0.618,
        "maxAC": 0.618,
        "minBD": 1.618,
        "maxBD": 1.618,
        "minXD": "-",
        "maxXD": "-",
    },
    {
        "pattern": "ideal butterfly",
        "minXB": 0.786,
        "maxXB": 0.786,
        "minAC": 0.618,
        "maxAC": 0.786,
        "minBD": 1.618,
        "maxBD": 1.618,
        "minXD": 1.272,
        "maxXD": 1.618,
    },
    {
        "pattern": "618 butterfly",
        "minXB": 0.786,
        "maxXB": 0.786,
        "minAC": 0.382,
        "maxAC": 0.786,
        "minBD": 1.618,
        "maxBD": 2.618,
        "minXD": 1.618,
        "maxXD": 1.618,
    },
    {
        "pattern": "gartley",
        "minXB": 0.618,
        "maxXB": 0.618,
        "minAC": 0.382,
        "maxAC": 0.886,
        "minBD": 1.128,
        "maxBD": 1.618,
        "minXD": 0.786,
        "maxXD": 0.786,
    },
    {
        "pattern": "butterfly",
        "minXB": 0.786,
        "maxXB": 0.786,
        "minAC": 0.382,
        "maxAC": 0.886,
        "minBD": 1.618,
        "maxBD": 2.236,
        "minXD": 1.272,
        "maxXD": 1.272,
    },
    {
        "pattern": "crab",
        "minXB": 0.382,
        "maxXB": 0.618,
        "minAC": 0.382,
        "maxAC": 0.886,
        "minBD": 2.618,
        "maxBD": 3.618,
        "minXD": 1.618,
        "maxXD": 1.618,
    },
    {
        "pattern": "deep crab",
        "minXB": 0.886,
        "maxXB": 0.886,
        "minAC": 0.382,
        "maxAC": 0.886,
        "minBD": 2.0,
        "maxBD": 3.618,
        "minXD": 1.618,
        "maxXD": 1.618,
    },
    {
        "pattern": "bat",
        "minXB": 0.382,
        "maxXB": 0.5,
        "minAC": 0.382,
        "maxAC": 0.886,
        "minBD": 1.618,
        "maxBD": 2.618,
        "minXD": 0.886,
        "maxXD": 0.886,
    },
    {
        "pattern": "alt bat",
        "minXB": 0.382,
        "maxXB": 0.382,
        "minAC": 0.382,
        "maxAC": 0.886,
        "minBD": 2.0,
        "maxBD": 3.618,
        "minXD": 1.128,
        "maxXD": 1.128,
    },
    {
        "pattern": "5-0",
        "minXB": 1.128,
        "maxXB": 1.618,
        "minAC": 1.618,
        "maxAC": 2.236,
        "minBD": 0.5,
        "maxBD": 0.5,
        "minXD": "-",
        "maxXD": "-",
    },
    {
        "pattern": "shark",
        "minXB": "-",
        "maxXB": "-",
        "minAC": 1.128,
        "maxAC": 1.618,
        "minBD": 1.618,
        "maxBD": 2.236,
        "minXD": 0.886,
        "maxXD": 0.886,
    },
    {
        "pattern": "shark",
        "minXB": "-",
        "maxXB": "-",
        "minAC": 1.128,
        "maxAC": 1.618,
        "minBD": 1.618,
        "maxBD": 2.236,
        "minXD": 1.128,
        "maxXD": 1.128,
    },
    {
        "pattern": "leonardo",
        "minXB": 0.5,
        "maxXB": 0.5,
        "minAC": 0.382,
        "maxAC": 0.886,
        "minBD": 1.128,
        "maxBD": 2.618,
        "minXD": 0.786,
        "maxXD": 0.786,
    },
    {
        "pattern": "nen star",
        "minXB": 0.382,
        "maxXB": 0.618,
        "minAC": 1.414,
        "maxAC": 2.14,
        "minBD": 1.128,
        "maxBD": 2.0,
        "minXD": 1.272,
        "maxXD": 1.272,
    },
    {
        "pattern": "cypher",
        "minXB": 0.382,
        "maxXB": 0.618,
        "minAC": 1.128,
        "maxAC": 1.414,
        "minBD": 1.272,
        "maxBD": 2.0,
        "minXD": 0.786,
        "maxXD": 0.786,
    },
    {
        "pattern": "3 drives",
        "minXB": 1.272,
        "maxXB": 1.272,
        "minAC": 0.618,
        "maxAC": 0.618,
        "minBD": 1.272,
        "maxBD": 1.272,
        "minXD": "-",
        "maxXD": "-",
    },
    {
        "pattern": "3 drives",
        "minXB": 1.618,
        "maxXB": 1.618,
        "minAC": 0.786,
        "maxAC": 0.786,
        "minBD": 1.618,
        "maxBD": 1.618,
        "minXD": "-",
        "maxXD": "-",
    },
    {
        "pattern": "perfect bat",
        "minXB": 0.5,
        "maxXB": 0.5,
        "minAC": 0.5,
        "maxAC": 0.618,
        "minBD": 2.0,
        "maxBD": 2.0,
        "minXD": 0.786,
        "maxXD": 0.886,
    },
]

anti_patterns = True

if anti_patterns:
    for i in range(len(XABCD_patterns)):
        XABCD_patterns.append(
            {
                "pattern": "anti " + XABCD_patterns[i]["pattern"],
                "minXB": 0.5,
                "maxXB": 0.5,
                "minAC": 0.5,
                "maxAC": 0.618,
                "minBD": 2.0,
                "maxBD": 2.0,
                "minXD": 0.786,
                "maxXD": 0.886,
            }
        )

        if XABCD_patterns[i]["minBD"] == "-" or XABCD_patterns[i]["maxBD"] == "-":
            XABCD_patterns[-1]["minXB"] = "-"
            XABCD_patterns[-1]["maxXB"] = "-"
        else:
            XABCD_patterns[-1]["minXB"] = round(1 / XABCD_patterns[i]["maxBD"], 3)
            XABCD_patterns[-1]["maxXB"] = round(1 / XABCD_patterns[i]["minBD"], 3)

        if XABCD_patterns[i]["minXB"] == "-" or XABCD_patterns[i]["maxXB"] == "-":
            XABCD_patterns[-1]["minBD"] = "-"
            XABCD_patterns[-1]["maxBD"] = "-"
        else:
            XABCD_patterns[-1]["minBD"] = round(1 / XABCD_patterns[i]["maxXB"], 3)
            XABCD_patterns[-1]["maxBD"] = round(1 / XABCD_patterns[i]["minXB"], 3)

        if XABCD_patterns[i]["minAC"] == "-" or XABCD_patterns[i]["maxAC"] == "-":
            XABCD_patterns[-1]["minAC"] = "-"
            XABCD_patterns[-1]["maxAC"] = "-"
        else:
            XABCD_patterns[-1]["minAC"] = round(1 / XABCD_patterns[i]["maxAC"], 3)
            XABCD_patterns[-1]["maxAC"] = round(1 / XABCD_patterns[i]["minAC"], 3)

        if XABCD_patterns[i]["minXD"] == "-" or XABCD_patterns[i]["maxXD"] == "-":
            XABCD_patterns[-1]["minXD"] = "-"
            XABCD_patterns[-1]["maxXD"] = "-"
        else:
            XABCD_patterns[-1]["minXD"] = round(1 / XABCD_patterns[i]["maxXD"], 3)
            XABCD_patterns[-1]["maxXD"] = round(1 / XABCD_patterns[i]["minXD"], 3)

print("HPQ: Harmonic Pattern Qualifier [by Artyom Shutoff]")

deviation = float(input("Deviation in %:")) / 100

deviationD = deviation

while True:
    possible_patterns = 0
    XB = float(input("XB:"))
    AC = float(input("AC:"))
    print("")

    XB_check, AC_check = 0, 0
    XB_old = XB
    AC_old = AC

    for i in fibo_type:
        if i == XB:
            XB_check = 1
            break

    for i in fibo_type:
        if i == AC:
            AC_check = 1
            break

    if not XB_check or not AC_check:
        for i in fibo_type:
            if XB_check and AC_check:
                break
            if not XB_check and i * (1 - deviation) <= XB <= i * (1 + deviation):
                XB = i
                XB_check = 1
            if not AC_check and i * (1 - deviation) <= AC <= i * (1 + deviation):
                AC = i
                AC_check = 1

    if XB_old != XB or AC_old != AC:
        print(f"XB {XB} AC {AC}\n")

    if XB_check and AC_check:
        for pattern in XABCD_patterns:
            XB_check, AC_check, BDcheck, XDcheck = 0, 0, 0, 0

            if not ("-" in (pattern["minXB"], pattern["maxXB"])):
                if pattern["minXB"] == pattern["maxXB"]:
                    if pattern["minXB"] == XB:
                        XB_check = 1
                    else:
                        continue

                else:
                    for i in fibo_type:
                        if i > pattern["maxXB"]:
                            break
                        if pattern["minXB"] < i < pattern["maxXB"]:
                            if i * (1 - deviation) <= XB <= i * (1 + deviation):
                                XB_check = 1
                                break

                    if XB_check != 1:
                        if (
                            pattern["minXB"] * (1 - deviation)
                            <= XB
                            <= pattern["minXB"] * (1 + deviation)
                        ):
                            XB_check = 1
                        if (
                            pattern["maxXB"] * (1 - deviation)
                            <= XB
                            <= pattern["maxXB"] * (1 + deviation)
                        ):
                            XB_check = 1

                    if XB_check != 1:
                        continue

            else:
                XB_check = 1

            if not (pattern["minAC"] == "-" or pattern["maxAC"] == "-"):
                if pattern["minAC"] == pattern["maxAC"]:
                    if pattern["minAC"] == AC:
                        AC_check = 1
                    else:
                        continue
                else:
                    for i in fibo_type:
                        if i > pattern["maxAC"]:
                            break
                        if pattern["minAC"] < i < pattern["maxAC"]:
                            if i * (1 - deviation) <= AC <= i * (1 + deviation):
                                AC_check = 1
                                break
                    if AC_check != 1:
                        if (
                            pattern["minAC"] * (1 - deviation)
                            <= AC
                            <= pattern["minAC"] * (1 + deviation)
                        ):
                            AC_check = 1
                        if (
                            pattern["maxAC"] * (1 - deviation)
                            <= AC
                            <= pattern["maxAC"] * (1 + deviation)
                        ):
                            AC_check = 1
                    if AC_check != 1:
                        continue
            else:
                AC_check = 1

            if (
                pattern["minBD"] != pattern["maxBD"]
                and pattern["minXD"] != pattern["maxXD"]
            ):
                if not (pattern["minBD"] == "-" or pattern["maxBD"] == "-"):
                    if pattern["minBD"] == pattern["maxBD"]:
                        BDcheck = 1
                        B = 1 - (1 * XB)
                        C = B + XB * AC
                        BC = C - B

                        D = C - BC * pattern["minBD"]
                        XD = (1 - D) / 1
                        if not (pattern["minXD"] == "-" or pattern["maxXD"] == "-"):
                            if pattern["minXD"] == pattern["maxXD"]:
                                if (
                                    pattern["minXD"] * (1 - deviationD)
                                    <= XD
                                    <= pattern["maxXD"] * (1 + deviationD)
                                ):
                                    XDcheck = 1
                                else:
                                    continue
                            else:
                                for i in fibo_type:
                                    if i > pattern["maxXD"]:
                                        break
                                    if pattern["minXD"] < i < pattern["maxXD"]:
                                        if (
                                            i * (1 - deviationD)
                                            <= XD
                                            <= i * (1 + deviationD)
                                        ):
                                            XDcheck = 1
                                            break

                                if XDcheck != 1:
                                    if (
                                        pattern["minXD"] * (1 - deviationD)
                                        <= XD
                                        <= pattern["minXD"] * (1 + deviationD)
                                    ):
                                        XDcheck = 1
                                    if (
                                        pattern["maxXD"] * (1 - deviationD)
                                        <= XD
                                        <= pattern["maxXD"] * (1 + deviationD)
                                    ):
                                        XDcheck = 1
                                if XDcheck != 1:
                                    continue

                        else:
                            XDcheck = 1

                    else:
                        if not (pattern["minXD"] == "-" or pattern["maxXD"] == "-"):
                            XDcheck = 1
                            B = 1 - (1 * XB)
                            C = B + XB * AC
                            BC = C - B
                            D = 1 - 1 * pattern["minXD"]
                            BD = (C - D) / BC

                            if pattern["minBD"] == pattern["maxBD"]:
                                if (
                                    pattern["minBD"] * (1 - deviationD)
                                    <= BD
                                    <= pattern["maxBD"] * (1 + deviationD)
                                ):
                                    BDcheck = 1
                                else:
                                    continue

                            else:
                                for i in fibo_type:
                                    if i > pattern["maxBD"]:
                                        break
                                    if pattern["minBD"] < i < pattern["maxBD"]:
                                        if (
                                            i * (1 - deviationD)
                                            <= BD
                                            <= i * (1 + deviationD)
                                        ):
                                            BDcheck = 1
                                            break
                                    if BDcheck != 1:
                                        if (
                                            pattern["minBD"] * (1 - deviationD)
                                            <= BD
                                            <= pattern["minBD"] * (1 + deviationD)
                                        ):
                                            BDcheck = 1
                                        if (
                                            pattern["maxBD"] * (1 - deviationD)
                                            <= BD
                                            <= pattern["maxBD"] * (1 + deviationD)
                                        ):
                                            BDcheck = 1
                                    if BDcheck != 1:
                                        continue
                        else:
                            XDcheck = 1
                else:
                    BDcheck = 1
                    XDcheck = 1

            else:
                BDcheck = 1
                XDcheck = 1

            if all([XB_check, AC_check, BDcheck, XDcheck]):
                if (
                    pattern["minBD"] != pattern["maxBD"]
                    and pattern["minXD"] != pattern["maxXD"]
                ):
                    print(
                        "Pattern:",
                        '"' + pattern["pattern"] + '"',
                        "BD:",
                        str(pattern["minBD"]) + "-" + str(pattern["maxBD"]),
                        "XD:",
                        str(pattern["minXD"]) + "-" + str(pattern["maxXD"]),
                    )
                if (
                    pattern["minBD"] == pattern["maxBD"]
                    and pattern["minXD"] == pattern["maxXD"]
                ):
                    print(
                        "Pattern:",
                        '"' + pattern["pattern"] + '"',
                        "BD:",
                        str(pattern["minBD"]),
                        "XD:",
                        str(pattern["minXD"]),
                    )
                if (
                    pattern["minBD"] != pattern["maxBD"]
                    and pattern["minXD"] == pattern["maxXD"]
                ):
                    print(
                        "Pattern:",
                        '"' + pattern["pattern"] + '"',
                        "BD:",
                        str(pattern["minBD"]) + "-" + str(pattern["maxBD"]),
                        "XD:",
                        str(pattern["minXD"]),
                    )
                if (
                    pattern["minBD"] == pattern["maxBD"]
                    and pattern["minXD"] != pattern["maxXD"]
                ):
                    print(
                        "Pattern:",
                        '"' + pattern["pattern"] + '"',
                        "BD:",
                        str(pattern["minBD"]),
                        "XD:",
                        str(pattern["minXD"]) + "-" + str(pattern["maxXD"]),
                    )
                print("")

                possible_patterns += 1

    if not possible_patterns:
        print("no pattern found")

    while True:
        out = input("exit? (Y/N):")
        if out.upper() in ["Y", "YES", "N", "NOT", "NO"]:
            break

    if out.upper() in ["Y", "YES"]:
        break

    else:
        print("-------------------")
        continue

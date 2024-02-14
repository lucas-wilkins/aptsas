from collections import defaultdict

from loadpos import PosData

class ParseError(Exception):
    pass

class LineCounter:
    """ Use for counting lines so that useful errors can be given"""
    def __init__(self, fid, verbose=False, max_lines=1000):
        self.fid = fid
        self.line_no = 0
        self.line = ""
        self.verbose = verbose
        self.max_lines = max_lines

    def next(self):
        line = self.fid.readline()

        # Check for EOF
        if line == "":
            if self.verbose:
                print(f" --- Last Line: {self.line_no} ---")
            raise StopIteration()

        self.line = line.strip()
        self.line_no += 1

        if self.verbose:
            print(f"{self.line_no}: {self.line}")

        if self.line_no > self.max_lines:
            raise ParseError("Max line count reached")

        return self.line


class Assigner:
    """ m/z assignment based on an .rrng file, reads a .rrng file and provides the `assign`
     method to apply the assigment"""
    def __init__(self, filename: str, verbose=False):

        self.elements: list[str] = []

        self.ranges: dict[str, list[tuple[float, float]]] = defaultdict(list)
        self.volumes: dict[str, float] = {} # Volumes of ions

        # Load the data, file looks toml like, but it's not toml
        with open(filename, 'r') as fid:

            counter = LineCounter(fid, verbose=verbose)

            try:

                while not counter.line.startswith("[Ions]"):
                    counter.next()
                    # print(counter.line)

                counter.next()  # Skip "Number=" line
                counter.next()  # ...and load the next one ready for the check

                while not counter.line.startswith("[Ranges]"):
                    self.elements.append(counter.line.strip().split("=")[1])
                    counter.next()

                # Line should now be the [Ranges] line
                counter.next() # Skip to the "Number=" line

                # Create the categorisation

                # while loop should be exited by StopIteration or by hitting max counter
                while True:

                    # Do .next first because we still have a line to skip, and because doing
                    # it at the start of a loop is a more maintainable place
                    counter.next()

                    # Ignore blank likes
                    if counter.line == "":
                        continue

                    # Store the line data:
                    # The format isn't quite optimal for what we want to do with it
                    # We want to know if we have a single ion or a cluster

                    after_eq = counter.line.split("=")[1]
                    tokens = after_eq.split()

                    start = float(tokens[0])
                    stop = float(tokens[1])

                    volume = 0.0

                    # Get the composition

                    components = []

                    for token in tokens[2:]:
                        if token.startswith("Vol:"):
                            volume = float(tokens[2].split(":")[1])
                            continue

                        if token.startswith("Color:"):
                            # Ignore this one
                            continue

                        parts = token.split(":")

                        element = parts[0]
                        count = int(parts[1])

                        components.append((element, count))

                    # Sort element symbols alphabetically, so make sure we have a unique representation of the ion
                    formula = "".join([el + str(n if n > 1 else "") for el, n in sorted(components, key=lambda x: x[0])])

                    self.volumes[formula] = volume
                    self.ranges[formula].append((start, stop))

            except StopIteration:
                pass # A good place to stop

            except Exception as e:

                raise ParseError(f"Parsing failed on line {counter.line_no}: '{counter.line.strip()}' -- {e}")

    def __repr__(self):
        s = ", ".join(self.elements)
        return f"{self.__class__.__name__}({s})"

    def assign(self, data: PosData):
        """ Apply the assignment to X,Y,Z,M/Z data (takes a PosData object)"""


# Intentionally obtuse

def part1(f):
    ranges = sorted(list(map(lambda r: tuple(map(int, r.split('-'))), open(f).read().strip().split(','))))

    def generate_invalid_ids():
        for k in range(1, 6):
            start_x = 1 if k == 1 else 10**(k-1)
            for x in range(start_x, 10**k):
                yield int(str(x) * 2)

    print(sum(filter(lambda inv_id: any(s <= inv_id <= e for s, e in ranges), generate_invalid_ids())))

if __name__ == "__main__":
    part1('example')
    part1('input')

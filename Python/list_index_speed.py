import arrow, timeit

def orig(az_el_series, rise_horizon_index, set_horizon_index):
    # MP would like us to include 3 minutes of below-horizon points in the azel series
    # https://jira.spaceflightindustries.com/browse/BSKY-8635
    delta_sec = 60 * 3
    rise_time = arrow.get(az_el_series[rise_horizon_index]['time'])
    set_time = arrow.get(az_el_series[set_horizon_index]['time'])

    # some defaults, should not need to use them but just in case
    start_index, stop_index = rise_horizon_index, set_horizon_index

    # convert to arrows once up front since we have to go through this twice below
    times = [arrow.get(azel['time']) for azel in az_el_series]

    # find the closest azel point that's delta_sec prior to rise time
    found = next((index for index, time in enumerate(times)
                  if index < rise_horizon_index and (rise_time - time).total_seconds() <= delta_sec), None)
    if found is not None:
        start_index = found

    found = next((index for index, time in enumerate(times)
                  if index > set_horizon_index and (time - set_time).total_seconds() >= delta_sec), None)
    if found is not None:
        stop_index = found

    return start_index, stop_index



def faster(az_el_series, rise_horizon_index, set_horizon_index):
    # MP would like us to include 3 minutes of below-horizon points in the azel series
    # https://jira.spaceflightindustries.com/browse/BSKY-8635
    delta_sec = 60 * 3
    rise_time = arrow.get(az_el_series[rise_horizon_index]['time'])
    set_time = arrow.get(az_el_series[set_horizon_index]['time'])

    # some defaults, should not need to use them but just in case
    start_index, stop_index = rise_horizon_index, set_horizon_index

    # convert to arrows once up front since we have to go through this twice below
    times = [arrow.get(azel['time']) for azel in az_el_series]

    # find the closest azel point that's delta_sec prior to rise time
    found = next((index for index, time in enumerate(reversed(times[:rise_horizon_index]))
                  if (rise_time - time).total_seconds() >= delta_sec), None)
    if found is not None:
        start_index = rise_horizon_index - 1 - found

    found = next((index for index, time in enumerate(times[set_horizon_index + 1:])
                  if (time - set_time).total_seconds() >= delta_sec), None)
    if found is not None:
        stop_index = found + set_horizon_index + 1

    return start_index, stop_index



az_el = [{"azimuth_degrees": 145 + i / 10,
          "elevation_degrees": 49 - ((i / 10) ** 2),
          "range_velocity_mks": 3000 + i,
          "time": arrow.get("2017-03-17T21:25").shift(seconds=5 * i).isoformat()}
            for i in range(-150, 150)]

r_i = 50
s_i = 245

def wrapper(func, *args, **kwargs):
     def wrapped():
         return func(*args, **kwargs)
     return wrapped

print("Original")
wrapped = wrapper(orig, az_el, r_i, s_i)
print(timeit.timeit(wrapped, number=500))

print("Faster?")
wrapped = wrapper(faster, az_el, r_i, s_i)
print(timeit.timeit(wrapped, number=500))

print("accuracy checks")
for i in range(50, 100, 5):
    for j in range(225, 275, 5):
        o = orig(az_el, i, j)
        f = faster(az_el, i, j)
        assert o == f, f"{o} vs {f}"
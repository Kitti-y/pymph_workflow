import pandas as pd
import os
import mph

import multiprocessing as mp

df1_read = pd.read_csv('coordinates_spreadsheets\\251118_coor_grid6_3_6_6_nonzero.csv')

#df_subset = df1_read.iloc[0:6]
#df_subset = df1_read.iloc[6:60]
#df_subset = df1_read.iloc[60:160]

#df_subset = df1_read.iloc[4:104]
#df_subset = df1_read.iloc[104:404]
#df_subset = df1_read.iloc[404:804]
df_subset = df1_read.iloc[804:-1]
# filename = 'template_ellipsoid_GAGs.mph'
def run_comsol_job(job):

    client = mph.start()
    model = client.load('template_ellipsoid_GAGs_lite.mph')

    modeljava = model.java

    geom_param, outputtag = job

    # model = mph.load(filename)   # load base model

    # 1. Set geometry params
    for k, v in geom_param.items():
        #model.parameter(k, v)
        modeljava.param().set(k, v)

    # 2. Update the geometry
    #model.geom("geom1").run()
    modeljava.component('comp1').geom('geom1').run()

    # 3. Set physics parameters
    # for k, v in phys_param.items():
    #     model.parameter(k, v)

    # 4. Solve
    #model.solve()
    modeljava.study('std1').run()

    # 5. Save output
    outname = f"run_test2/251120_ellipsoid_GAGs_{outputtag}.mph"
    model.save(outname)

    model.clear()
    client.clear()

    return outname

if __name__ == "__main__":

    jobs = []

    for index, row in df_subset.iterrows():

        r_coord = row['r']
        xdeg_coord = row['x_deg']
        tdeg_coord = row['t_deg']
        pdeg_coord = row['p_deg']

        r_index = int(row['nr'])
        x_index = int(row['nx'])
        t_index = int(row['nt'])
        p_index = int(row['np'])

        jobs.append(
            (
                {"rposition": str(r_coord),           
                "angle_xi": str(xdeg_coord),
                "angle_theta": str(tdeg_coord),
                "angle_phi": str(pdeg_coord)},
                f'{r_index}{x_index}{t_index}{p_index}'
            )
        )

    NPROC = 4  # Use number less than your CPU count to avoid overload

    with mp.Pool(processes=NPROC) as pool:
        results = pool.map(run_comsol_job, jobs)

    print("All COMSOL jobs done:")

    # open text file to write results
    with open('251120_mp_comsol_results.txt', 'a') as f:
        for r in results:
            f.write(f"{r}\n")

    for r in results:
        print(r)
import pandas as pd
import os
import mph
import numpy as np

extracted_results = []

for files in os.listdir('D:\\run_test2'):
    if files.endswith('.mph'):
        filepath = os.path.join('D:\\run_test2', files)

        client = mph.start()
        model = client.load(filepath)
        modeljava = model.java

        modeljava.result().numerical().create("int1", "IntSurface")
        modeljava.result().numerical("int1").selection().named("sel1")
        modeljava.result().numerical("int1").setIndex("expr", "Sigma_s*V/qe*L_scale*L_scale", 0)
        modeljava.result().numerical("int1").run()

        G_on_C = modeljava.result().numerical("int1").getReal()

        modeljava.result().numerical().create("int2", "IntSurface")
        modeljava.result().numerical("int2").selection().named("sel2")
        modeljava.result().numerical("int2").setIndex("expr", "Sigma_c*V/qe*L_scale*L_scale", 0)
        modeljava.result().numerical("int2").run()

        G_on_S = modeljava.result().numerical("int2").getReal()

        client.clear()

        array_result1 = np.array(G_on_C)
        array_result2 = np.array(G_on_S)
        flatten_arr = (array_result1+array_result2).flatten()

        # calculate integration over alpha

        resq1 = 0
        resq2 = 0
        resq3 = 0

        weight = [ 0.83333333, 0.83333333, 0.16666667]
        resq1 = 0.5*(weight*flatten_arr[0:3]).sum()
        resq2 = 0.5*(weight*flatten_arr[3:6]).sum()
        resq3 = 0.5*(weight*flatten_arr[6:9]).sum()

        extracted_results.append(
            {"path": filepath, "G_ch1": resq1, "G_ch2": resq2, "G_ch3" : resq3}
            )
        
df_results = pd.DataFrame(extracted_results)
#df_results.to_csv('251120_mp_extracted_results.csv', index=False)
#df_results.to_csv('251120_mp_extracted_results.csv', index=False)
df_results.to_csv('251125_mp_extracted_results_2.csv', index=False)

#import multiprocessing as mp

#df1_read = pd.read_csv('coordinates_spreadsheets\\251118_coor_grid6_3_6_6_nonzero.csv')

#df_subset = df1_read.iloc[0:6]
#df_subset = df1_read.iloc[6:60]
# df_subset = df1_read.iloc[60:160]

# # filename = 'template_ellipsoid_GAGs.mph'
# def run_comsol_job(job):

#     client = mph.start()
#     model = client.load('template_ellipsoid_GAGs_lite.mph')

#     modeljava = model.java

#     geom_param, outputtag = job

#     # model = mph.load(filename)   # load base model

#     # 1. Set geometry params
#     for k, v in geom_param.items():
#         #model.parameter(k, v)
#         modeljava.param().set(k, v)

#     # 2. Update the geometry
#     #model.geom("geom1").run()
#     modeljava.component('comp1').geom('geom1').run()

#     # 3. Set physics parameters
#     # for k, v in phys_param.items():
#     #     model.parameter(k, v)

#     # 4. Solve
#     #model.solve()
#     modeljava.study('std1').run()

#     # 5. Save output
#     outname = f"run_test2/251120_ellipsoid_GAGs_{outputtag}.mph"
#     model.save(outname)

#     model.clear()
#     client.clear()

#     return outname

# if __name__ == "__main__":

#     jobs = []

#     for index, row in df_subset.iterrows():

#         r_coord = row['r']
#         xdeg_coord = row['x_deg']
#         tdeg_coord = row['t_deg']
#         pdeg_coord = row['p_deg']

#         r_index = int(row['nr'])
#         x_index = int(row['nx'])
#         t_index = int(row['nt'])
#         p_index = int(row['np'])

#         jobs.append(
#             (
#                 {"rposition": str(r_coord),           
#                 "angle_xi": str(xdeg_coord),
#                 "angle_theta": str(tdeg_coord),
#                 "angle_phi": str(pdeg_coord)},
#                 f'{r_index}{x_index}{t_index}{p_index}'
#             )
#         )

#     NPROC = 3  # Use number less than your CPU count to avoid overload

#     with mp.Pool(processes=NPROC) as pool:
#         results = pool.map(run_comsol_job, jobs)

#     print("All COMSOL jobs done:")
#     for r in results:
#         print(r)
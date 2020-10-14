import numpy as np
import math

def model(N_total, cloud_optical_thickness, cloud_scattering_albedo, solar_zenith_angle):
    N_ref = 0
    N_tra = 0
    N_abs = 0
    eeta = np.random.rand(N_total)
    photons = {}
    reflected_photons = {}
    absorbed_photons  ={}
    transmitted = {}
    depth_records = {}

    for photon in range(N_total):
        print("[photon] ", photon)
        dead = 0
        initial_tmp_thickness = cloud_optical_thickness
        theta = solar_zenith_angle
        scatter_counter = 0
        depth = []

        while not dead:
            if solar_zenith_angle < 0:
                N_ref += 1
                reflected_photons[photon] = scatter_counter
                dead = 1

            elif solar_zenith_angle > cloud_optical_thickness:
                N_tra += 1
                transmitted[photon] = scatter_counter
                dead = 1

            elif 0 < solar_zenith_angle < cloud_optical_thickness:
                scattered = eeta[photon] <= cloud_scattering_albedo
                absorbed = eeta[photon] > cloud_scattering_albedo
                if scattered:
                    scatter_counter += 1
                    photons[photon] = scatter_counter

                    L = - math.log(1 - eeta[photon])
                    mu = 2 * eeta[photon] - 1
                    theta_next = theta + math.acos(mu)

                    y = initial_tmp_thickness
                    y_next = y + L * math.cos(theta_next)
                    theta = theta_next
                    initial_tmp_thickness = y_next
                    print(y_next)
                    depth.append(y_next)

                    if y_next < 0:
                        N_ref += 1
                        reflected_photons[photon] = scatter_counter
                        dead = 1

                    elif y_next > cloud_optical_thickness:
                        N_tra += 1
                        transmitted[photon] = scatter_counter
                        dead = 1

                    elif 0 <= y_next <= cloud_optical_thickness:
                        dead = 0

                elif absorbed:
                    N_abs += 1
                    absorbed_photons[photon] = scatter_counter
                    dead = 1

        if scatter_counter == 1:
            N_ref +=1
            reflected_photons[photon] = scatter_counter

        depth_records[photon] = depth
        depth = []
        #cloud_optical_thickness = initial_tmp_thickness
    N_tra = N_total - (N_ref + N_abs)

    R = N_ref / N_total
    A = N_abs / N_total
    T = N_tra / N_total

    return N_ref, N_abs, N_tra, R, A, T, photons, reflected_photons, absorbed_photons, transmitted, depth_records

if __name__ == "__main__":
    N_total = 100
    cloud_optical_thickness = 10  # 50, 10
    cloud_scattering_albedo = 1.0  # 0.9, 1.0
    solar_zenith_angle = 0.0001  # 0.1
    N_ref, N_abs, N_tra, R, A, T, photons, reflected_photons, absorbed_photons, transmitted, depth_records = model(N_total, cloud_optical_thickness, cloud_scattering_albedo, solar_zenith_angle)

    with open("q1_answer.txt", "w") as f:
        for photon in photons:
            print("[photon] {} scattered {} times.".format(photon, photons[photon]))
            f.write("[photon] {} scattered {} times.\n".format(photon, photons[photon]))
        print("Number of photons reflected: ", N_ref)
        print("Number of absorbed photons: ", N_abs)
        print("Number of transmitted photons: ", N_tra)
        print("Reflection: ", R)
        print("Absorption: ", A)
        print("Transmission: ", T)
        f.write("Number of photons reflected: "+ str(N_ref)+'\n')
        f.write("Number of absorbed photons: "+ str(N_abs)+'\n')
        f.write("Number of transmitted photons: "+ str(N_tra)+'\n')
        f.write("Reflection: "+ str(R)+'\n')
        f.write("Absorption: "+ str(A)+'\n')
        f.write("Transmission: "+ str(T)+'\n')

    #print(reflected_photons.keys())
    #print(absorbed_photons.keys())
    #print(transmitted.values())
    c = list(set(transmitted.values()))
    #print(len(c))

    normal_dist = {}
    for i in c:
        count = 0
        for photon in transmitted:
            if transmitted[photon] == i:
                count += 1
        normal_dist[i] = count

    print(normal_dist)
    R = 0
    probs = []
    for i in normal_dist:
        R += normal_dist[i]/sum(normal_dist.values())
        probs.append(normal_dist[i]/sum(normal_dist.values()))
    # print(len(probs))
    with open("q2_answer.txt", "w") as f:
        print("[probabilities]", probs)
        print("[Check sum = 1 ?]", round(R))
        f.write("[probabilities]"+ str(probs)+'\n')
        f.write("[Check sum = 1 ?]"+ str(round(R))+'\n')


    print(depth_records)
    with open("q3_answer.txt", "w") as f:
        for record in depth_records:
            print('[photon] {}: max depth: {}'.format(record, max(depth_records[record])))
            f.write('[photon] {}: max depth: {}\n'.format(record, max(depth_records[record])))
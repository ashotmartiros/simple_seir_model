import argparse
import matplotlib.pyplot as plt

NUMBER_OF_STEPS = 10 
def parse_arguments():
    parser = argparse.ArgumentParser()

    parser.add_argument("-s", "--susceptuble", type=int, required=True, help="Initial susceptible count.")
    parser.add_argument("-e", "--exposed", type=int, required=True, help="Initial exposed count.")
    parser.add_argument("-i", "--infected", type=int, required=True, help="Initial infected count.")
    parser.add_argument("-r", "--recovered", type=int, required=True, help="Initial recovered count.")
    parser.add_argument("-be", "--beta", type=float, required=True, help="Initial beta coefficent.")
    parser.add_argument("-ga", "--gamma", type=float, required=True, help="Initial gamma coefficent.")
    parser.add_argument("-si", "--sigma", type=float, required=True, help="Initial sigma coeffincent.")
    parser.add_argument("-d", "--day", type=int, required=True, help="Number of days.")
    return parser.parse_args()

class SEIR:
    def __init__(self, susceptuble
                     , exposed
                     , infected
                     , recovered
                     , beta
                     , gamma
                     , sigma
                     , day):
        self.day_ = day
        self.susceptubles_ = [susceptuble] + [0] * self.day_ * NUMBER_OF_STEPS 
        self.exposeds_ = [exposed] + [0] * self.day_ * NUMBER_OF_STEPS 
        self.infecteds_ = [infected] + [0] * self.day_ * NUMBER_OF_STEPS 
        self.recovereds_ = [recovered] + [0] * self.day_ * NUMBER_OF_STEPS 
        self.beta_ = beta 
        self.gamma_ = gamma
        self.sigma_ = sigma
        self.N_ = susceptuble + exposed + infected + recovered

    def update_(self, i, h):
        s_i = self.susceptubles_[i]
        e_i = self.exposeds_[i]
        i_i = self.infecteds_[i]
        r_i = self.recovereds_[i]

        k1 = -(self.beta_/self.N_) * s_i * i_i
        n1 = (self.beta_/self.N_) * s_i * i_i - self.sigma_ * e_i
        l1 = self.sigma_ * e_i - self.gamma_ * i_i
        m1 = self.gamma_ * i_i 

        k2 = -(self.beta_/self.N_) * (i_i + n1 * (h / 2)) * (s_i + k1 * (h / 2))
        n2 = (self.beta_/self.N_) * (i_i + n1 * (h / 2)) * (s_i + k1 * (h / 2)) - self.sigma_ * (e_i + n1 * (h / 2))
        l2 = self.sigma_ * (e_i + n1 * (h / 2))- self.gamma_ * (i_i + l1 * (h / 2))
        m2 = self.gamma_ * (i_i + l1 * (h / 2)) 

        k3 = -(self.beta_/self.N_) * (i_i + n2 * (h / 2)) * (s_i + k2 * (h / 2))
        n3 = (self.beta_/self.N_) * (i_i + n2 * (h / 2)) * (s_i + k2 * (h / 2)) - self.sigma_ * (e_i + n2 * (h / 2))
        l3 = self.sigma_ * (e_i + n2 * (h / 2))- self.gamma_ * (i_i + l2 * (h / 2))
        m3 = self.gamma_ * (i_i + l2 * (h / 2)) 

        k4 = -(self.beta_/self.N_) * (i_i + n3 * h) * (s_i + k3 * h)
        n4 = (self.beta_/self.N_) * (i_i + n3 * h) * (s_i + k3 * h) - self.sigma_ * (e_i + n3 * h)
        l4 = self.sigma_ * (e_i + n3 * h)- self.gamma_ * (i_i + l3 * h)
        m4 = self.gamma_ * (i_i + l3 * h) 

        self.susceptubles_[i+1] = s_i + (h/6) * (k1 + 2*k2 + 2*k3 + k4)
        self.exposeds_[i+1] = e_i + (h/6) * (n1 + 2*n2 + 2*n3 + n4)
        self.infecteds_[i+1] = i_i + (h/6) * (l1 + 2*l2 + 2*l3 + l4)
        self.recovereds_[i+1] = r_i + (h/6) * (m1 + 2*m2 + 2*m3 + m4)
    
    def solve(self):
        h = 1 / NUMBER_OF_STEPS
        idx = 0
        ts = 0
        self.time_stamp_ = [ts]
        for day in range(self.day_):
            for step in range(NUMBER_OF_STEPS):
                self.update_(idx, h)
                idx += 1
                ts += h
                self.time_stamp_.append(ts)
        #print("Susceptubles: ", self.susceptubles_)
        #print("Exposeds: ", len(self.exposeds_))
        #print("Infencteds: ", len(self.infecteds_))
        #print("Recovereds: ", len(self.recovereds_))

    def draw(self, path=''):
        plt.plot(self.time_stamp_, self.susceptubles_, label = 'susceptubles')
        plt.plot(self.time_stamp_, self.exposeds_, label = 'exposeds')
        plt.plot(self.time_stamp_, self.infecteds_, label = 'infecteds')
        plt.plot(self.time_stamp_, self.recovereds_, label = 'recovereds')
        plt.xlabel('Days')
        plt.ylabel('Population')
        plt.title('SEIR model demostration.')
        plt.legend()
        if not path:
            plt.show()
        plt.savefig(path)
        plt.clf()

def main(args):
    seir_model = SEIR(args.susceptuble
                     ,args.exposed 
                     ,args.infected
                     ,args.recovered
                     ,args.beta
                     ,args.gamma
                     ,args.sigma
                     ,args.day)
    seir_model.solve()
    seir_model.draw()

if __name__ == "__main__":
    args = parse_arguments()
    main(args)


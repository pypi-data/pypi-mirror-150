import wrapper as pyw

r=3
n=3
env = pyw.fm_init( n)

A = pyw.ShowCoalitions( env)
print( "Fuzzy measure wrt n=3 criteria has ",env.m," parameters ordered like this (binary order)")
print( A)
pyw.fm_free( env);

ti=1
n=4
env = pyw.fm_init( n);
size, v = pyw.generate_fm_2additive_concave( ti,n, env)
print( "2-additive concave FM in Mobius and its length (n=4)")
print( v)
print("has ", size, " nonzero parameters ")

print("A convex FM in cardinality ordering ")
A = pyw.ShowCoalitionsCard( env)
print( A)

size, v = pyw.generate_fmconvex_tsort( ti, n, n-1 , 1000, 8, 1, env)
print( v)
print("has ", size, " nonzero parameters ")

vb = pyw.ConvertCard2Bit( v, env)

print("a convex FM in binary ordering ")
A = pyw.ShowCoalitions( env)
print( A)
print( vb)

r = pyw.IsMeasureSupermodular( vb, env)
print( "Is it convex (test)?", r)
r = pyw.IsMeasureAdditive( vb, env)
print("Is it additive (test)?", r)

mc = pyw.export_maximal_chains( n, vb, env)
print( "Export maximal chains ")
print( mc)

x = [0.2,0.1,0.6,0.2]
z = pyw.Choquet( x, vb, env)
print( "Choquet integral of ",x, " is ",z)

z = pyw.Sugeno( x, vb, env)
print("Sugeno integral of ",x,  " is ",z)


###
# Test generated wrapper
###

# Test wrapper for:
#    double py_ChoquetKinter(double* x, double* v, int kint, struct fm_env* env)
x = [0.2,0.5,0.4]
v = [0,0.3,0.5,0.6,0.4,0.8,0.7,1]
kint = 2
r = pyw.ChoquetKinter( x, v, kint, env)
print( "Choquet integral of: ", kint, x, v)
print( "equals: ", r)

# Test wrapper for:
#    double py_Orness(double* Mob, struct fm_env* env)
v = [0,0.3,0.5,0.6,0.4,0.8,0.7,1]
r = pyw.Orness(v, env)
print( "orness value of the Choquet integral wrt fuzzy measure v: ", v)
print( "equals: ", r)

# Test wrapper for:
#    void py_NonmodularityIndexKinteractive(double* v, double* out_w, int kint,  struct fm_env* env)
kint = 2
v = [0,0.3,0.5,0.6,0.4,0.8,0.7,1]
pnm = pyw.NonmodularityIndexKinteractive( v, kint, env)
print( "nonmodularity indices of k-interactive fuzzy measure v: ", kint, v)
print( "equals: ", pnm)


# Test wrapper for:
#    double py_min_subset(double* x, int n, int_64 S)
# pyw.min_subset(x, n, S)
# not documented

# Test wrapper for:
#    double py_max_subset(double* x, int n, int_64 S)
# pyw.max_subset(x, n, S)
# not documented

# Test wrapper for:
#    double py_min_subsetC(double* x, int n, int_64 S, struct fm_env* env)
# pyw.min_subsetC(x, n, S, env)
# not documented

# Test wrapper for:
#    double py_max_subsetNegC(double* x, int n, int_64 S, struct fm_env* env)
# pyw.max_subsetNegC(x, n, S, env)
# not documented


# Test wrapper for:
#    int py_SizeArraykinteractive(int n, int k, struct fm_env* env)
# pyw.SizeArraykinteractive(n, k, env)
# not documented


# Test wrapper for:
#    int py_IsSubsetC(int i, int j, struct fm_env* env)
# pyw.IsSubsetC(i, j, env)
# not documented

# Test wrapper for:
#    int py_IsElementC(int i, int j, struct fm_env* env)
# pyw.IsElementC(i, j, env)
# not documented

# Test wrapper for:
#    void py_ExpandKinteractive2Bit(double* out_dest, double* src, struct fm_env* env, int kint, int arraysize)
# pyw.ExpandKinteractive2Bit(src, env, kint, arraysize)
# not documented


# Test wrapper for:
#    void py_ExpandKinteractive2Bit_m(double* out_dest, double* src, struct fm_env* env, int kint, int arraysize, double* VVC)
# pyw.ExpandKinteractive2Bit_m(src, env, kint, arraysize, VVC)
# not documented

# Test wrapper for:
#    void py_Shapley(double* v, double* out_x, struct fm_env* env)
# pyw.Shapley(v, env)
v = [0,0.3,0.5,0.6,0.4,0.8,0.7,1]
x = pyw.Shapley( v, env)
print( "v: ", v)
print( "x: ", x)

# Test wrapper for:
#    void py_Banzhaf(double* v, double* out_B, struct fm_env* env)
v =[0.0,0.3,0.5,-0.2,0.4,0.1,-0.2,0.1]
x = pyw.Banzhaf(v, env)
print( "v: ", v)
print( "x: ", x)


# Test wrapper for:
#    void py_ShapleyMob(double* Mob, double* out_x, struct fm_env* env)
Mob = [0.0,0.3,0.5,-0.2,0.4,0.1,-0.2,0.1]
x = pyw.ShapleyMob( Mob, env)
print( "Mob: ", Mob)
print( "x: ", x)


# Test wrapper for:
#    void py_BanzhafMob(double* Mob, double* out_B, struct fm_env* env)
Mob = [0.0,0.3,0.5,-0.2,0.4,0.1,-0.2,0.1]
x = pyw.BanzhafMob(Mob, env)
print( "Mob: ", Mob)
print( "x: ", x)


# Test wrapper for:
#    double py_ChoquetMob(double* x, double* Mob, struct fm_env* env)
x =[0.6,0.3,0.8]
Mob = [0.0,0.3,0.5,-0.2,0.4,0.1,-0.2,0.1]
c = pyw.ChoquetMob(x, Mob, env)
print( "Mob: ", Mob)
print( "x: ", x)
print( "Choquet integral: ", c )

# Test wrapper for:
#    void py_ConstructLambdaMeasure(double* singletons, double* out_lambdax, double* out_v, struct fm_env* env)
singletons = [0, 0.3, 0.5]
lambdax, v = pyw.ConstructLambdaMeasure(singletons, env)
print( "singletons: ", singletons)
print( "lambdax, v: ", lambdax, v)


# Test wrapper for:
#    void py_ConstructLambdaMeasureMob(double* singletons, double* out_lambdax, double* out_Mob, struct fm_env* env)
singletons = [0, 0.3, 0.5]
lambdax, Mob = pyw.ConstructLambdaMeasureMob(singletons, env)
print( "singletons: ", singletons)
print( "lambdax, Mob: ", lambdax, Mob)


# Test wrapper for:
#    void py_dualm(double* v, double* out_w, struct fm_env* env)
# pyw.dualm(v, env)


# Test wrapper for:
#    void py_dualmMob(double* v, double* out_w, struct fm_env* env)
# pyw.dualmMob(v, env)


# Test wrapper for:
#    double py_Entropy(double* v, struct fm_env* env)
# pyw.Entropy(v, env)


# Test wrapper for:
#    void py_FuzzyMeasureFit(int datanum, int additive, struct fm_env* env, double* out_v, double* dataset)
# pyw.FuzzyMeasureFit(datanum, additive, env, dataset)


# Test wrapper for:
#    void py_FuzzyMeasureFitMob(int datanum, int additive, struct fm_env* env, double* out_v, double* dataset)
# pyw.FuzzyMeasureFitMob(datanum, additive, env, dataset)


# Test wrapper for:
#    void py_FuzzyMeasureFitKtolerant(int datanum, int additive, struct fm_env* env, double* out_v, double* dataset)
# pyw.FuzzyMeasureFitKtolerant(datanum, additive, env, dataset)


# Test wrapper for:
#    void py_FuzzyMeasureFitLPKmaxitive(int datanum, int additive, struct fm_env* env, double* out_v, double* dataset)
# pyw.FuzzyMeasureFitLPKmaxitive(datanum, additive, env, dataset)


# Test wrapper for:
#    void py_FuzzyMeasureFitLPKinteractive(int datanum, int additive, struct fm_env* env, double* out_v, double* dataset, double* K)
# pyw.FuzzyMeasureFitLPKinteractive(datanum, additive, env, dataset, K)


# Test wrapper for:
#    void py_FuzzyMeasureFitLPKinteractiveMaxChains(int datanum, int additive, struct fm_env* env, double* out_v, double* dataset, double* K)
# pyw.FuzzyMeasureFitLPKinteractiveMaxChains(datanum, additive, env, dataset, K)


# Test wrapper for:
#    void py_FuzzyMeasureFitLPKinteractiveAutoK(int datanum, int additive, struct fm_env* env, double* out_v, double* dataset, double* K, int* maxiters)
# pyw.FuzzyMeasureFitLPKinteractiveAutoK(datanum, additive, env, dataset, K, maxiters)


# Test wrapper for:
#    void py_FuzzyMeasureFitLPKinteractiveMarginal(int datanum, int additive, struct fm_env* env, double* out_v, double* dataset, double* K, int submod)
# pyw.FuzzyMeasureFitLPKinteractiveMarginal(datanum, additive, env, dataset, K, submod)


# Test wrapper for:
#    void py_FuzzyMeasureFitLPKinteractiveMarginalMaxChain(int datanum, int additive, struct fm_env* env, double* out_v, double* dataset, double* K, int* maxiters, int submod)
# pyw.FuzzyMeasureFitLPKinteractiveMarginalMaxChain(datanum, additive, env, dataset, K, maxiters, submod)


# Test wrapper for:
#    void py_FuzzyMeasureFitLP(int datanum, int additive, struct fm_env* env, double* out_v, double* dataset, int* options, double* indexlow, double* indexhihg, int* option1, double* orness)
# pyw.FuzzyMeasureFitLP(datanum, additive, env, dataset, options, indexlow, indexhihg, option1, orness)


# Test wrapper for:
#    void py_FuzzyMeasureFitLPMob(int datanum, int additive, struct fm_env* env, double* out_v, double* dataset, int* options, double* indexlow, double* indexhihg, int* option1, double* orness)
# pyw.FuzzyMeasureFitLPMob(datanum, additive, env, dataset, options, indexlow, indexhihg, option1, orness)


# Test wrapper for:
#    void py_fittingOWA(int datanum, struct fm_env* env, double* out_v, double* dataset)
# pyw.fittingOWA(datanum, env, dataset)


# Test wrapper for:
#    void py_fittingWAM(int datanum, struct fm_env* env, double* out_v, double* dataset)
# pyw.fittingWAM(datanum, env, dataset)


# Test wrapper for:
#    void py_Interaction(double* out_Mob, double* v, struct fm_env* env)
# pyw.Interaction(v, env)


# Test wrapper for:
#    void py_InteractionB(double* out_Mob, double* v, struct fm_env* env)
# pyw.InteractionB(v, env)


# Test wrapper for:
#    void py_InteractionMob(double* out_Mob, double* v, struct fm_env* env)
# pyw.InteractionMob(v, env)


# Test wrapper for:
#    void py_InteractionBMob(double* Mob, double* out_v, struct fm_env* env)
# pyw.InteractionBMob(Mob, env)


# Test wrapper for:
#    void py_BipartitionShapleyIndex(double* v, double* out_w, struct fm_env* env)
# pyw.BipartitionShapleyIndex(v, env)


# Test wrapper for:
#    void py_BipartitionBanzhafIndex(double* v, double* out_w, struct fm_env* env)
# pyw.BipartitionBanzhafIndex(v, env)


# Test wrapper for:
#    void py_BNonadditivityIndexMob(double* Mob, double* out_w, struct fm_env* env)
# pyw.BNonadditivityIndexMob(Mob, env)


# Test wrapper for:
#    void py_NonadditivityIndex(double* v, double* out_w, struct fm_env* env)
# pyw.NonadditivityIndex(v, env)


# Test wrapper for:
#    void py_NonmodularityIndex(double* v, double* out_w, struct fm_env* env)
# pyw.NonmodularityIndex(v, env)


# Test wrapper for:
#    void py_NonmodularityIndexMob(double* Mob, double* out_w, struct fm_env* env)
# pyw.NonmodularityIndexMob(Mob, env)


# Test wrapper for:
#    void py_NonmodularityIndexMobkadditive(double* Mob, double* out_w, int k,  struct fm_env* env)
# pyw.NonmodularityIndexMobkadditive(Mob, k, env)


# Test wrapper for:
#    int py_IsMeasureBalanced(double* v, struct fm_env* env)
# pyw.IsMeasureBalanced(v, env)


# Test wrapper for:
#    int py_IsMeasureSelfdual(double* v, struct fm_env* env)
# pyw.IsMeasureSelfdual(v, env)


# Test wrapper for:
#    int py_IsMeasureSubadditive(double* v, struct fm_env* env)
# pyw.IsMeasureSubadditive(v, env)


# Test wrapper for:
#    int py_IsMeasureSubmodular(double* v, struct fm_env* env)
# pyw.IsMeasureSubmodular(v, env)


# Test wrapper for:
#    int py_IsMeasureSuperadditive(double* v, struct fm_env* env)
# pyw.IsMeasureSuperadditive(v, env)


# Test wrapper for:
#    int py_IsMeasureSymmetric(double* v, struct fm_env* env)
# pyw.IsMeasureSymmetric(v, env)


# Test wrapper for:
#    int py_IsMeasureKMaxitive(double* v, struct fm_env* env)
# pyw.IsMeasureKMaxitive(v, env)


# Test wrapper for:
#    int py_IsMeasureAdditiveMob(double* Mob, struct fm_env* env)
# pyw.IsMeasureAdditiveMob(Mob, env)


# Test wrapper for:
#    int py_IsMeasureBalancedMob(double* Mob, struct fm_env* env)
# pyw.IsMeasureBalancedMob(Mob, env)


# Test wrapper for:
#    int py_IsMeasureSelfdualMob(double* Mob, struct fm_env* env)
# pyw.IsMeasureSelfdualMob(Mob, env)


# Test wrapper for:
#    int py_IsMeasureSubadditiveMob(double* Mob, struct fm_env* env)
# pyw.IsMeasureSubadditiveMob(Mob, env)


# Test wrapper for:
#    int py_IsMeasureSubmodularMob(double* Mob, struct fm_env* env)
# pyw.IsMeasureSubmodularMob(Mob, env)


# Test wrapper for:
#    int py_IsMeasureSuperadditiveMob(double* Mob, struct fm_env* env)
# pyw.IsMeasureSuperadditiveMob(Mob, env)


# Test wrapper for:
#    int py_IsMeasureSupermodularMob(double* Mob, struct fm_env* env)
# pyw.IsMeasureSupermodularMob(Mob, env)


# Test wrapper for:
#    int py_IsMeasureSymmetricMob(double* Mob, struct fm_env* env)
# pyw.IsMeasureSymmetricMob(Mob, env)


# Test wrapper for:
#    int py_IsMeasureKMaxitiveMob(double* Mob, struct fm_env* env)
# pyw.IsMeasureKMaxitiveMob(Mob, env)


# Test wrapper for:
#    void py_Mobius(double* v, double* out_MobVal, struct fm_env* env)
# pyw.Mobius(v, env)





# Test wrapper for:
#    double py_OWA(double* x, double* v, struct fm_env* env)
# pyw.OWA(x, v, env)


# Test wrapper for:
#    double py_WAM(double* x, double* v, struct fm_env* env)
# pyw.WAM(x, v, env)


# Test wrapper for:
#    void py_Zeta(double* Mob, double* out_v, struct fm_env* env)
# pyw.Zeta(Mob, env)


# Test wrapper for:
#    void py_dualMobKadd(int m, int length, int k, double* src, double* out_dest, struct fm_env* env)
# pyw.dualMobKadd(m, length, k, src, env)


# Test wrapper for:
#    void py_Shapley2addMob(double* v, double* out_x, int n)
# pyw.Shapley2addMob(v, n)


# Test wrapper for:
#    void py_Banzhaf2addMob(double* v, double* out_x, int n)
# pyw.Banzhaf2addMob(v, n)


# Test wrapper for:
#    double py_Choquet2addMob(double* x, double* Mob, int n)
# pyw.Choquet2addMob(x, Mob, n)


# Test wrapper for:
#    int py_fm_arraysize(int n, int kint, struct fm_env* env)
# pyw.fm_arraysize(n, kint, env)


# Test wrapper for:
#    int py_generate_fm_minplus(int num, int n, int kint, int markov, int option, double K, double* vv, struct fm_env* env)
# pyw.generate_fm_minplus(num, n, kint, markov, option, K, vv, env)


# Test wrapper for:
#    int py_generate_fm_2additive_convex(int num, int n,  double* vv)
# pyw.generate_fm_2additive_convex(num, n, vv)


# Test wrapper for:
#    int py_generate_fm_2additive_convex_withsomeindependent(int num, int n, double* vv)
# pyw.generate_fm_2additive_convex_withsomeindependent(num, n, vv)


# Test wrapper for:
#    void py_prepare_fm_sparse(int n, int tupsize, int* tuples, struct fm_env_sparse* out_env)
# pyw.prepare_fm_sparse(n, tupsize, tuples, out_env)


# Test wrapper for:
#    int py_tuple_cardinality_sparse(int i, struct fm_env_sparse* env)
# pyw.tuple_cardinality_sparse(i, env)


# Test wrapper for:
#    int py_get_num_tuples(struct fm_env_sparse* env)
# pyw.get_num_tuples(env)


# Test wrapper for:
#    int py_get_sizearray_tuples(struct fm_env_sparse* env)
# pyw.get_sizearray_tuples(env)


# Test wrapper for:
#    int py_is_inset_sparse(int A, int card, int i, struct fm_env_sparse* env)
# pyw.is_inset_sparse(A, card, i, env)


# Test wrapper for:
#    int py_is_subset_sparse(int A, int cardA, int B, int cardB, struct fm_env_sparse* env)
# pyw.is_subset_sparse(A, cardA, B, cardB, env)


# Test wrapper for:
#    double py_min_subset_sparse(double* x, int n, int S, int cardS, struct fm_env_sparse* env)
# pyw.min_subset_sparse(x, n, S, cardS, env)


# Test wrapper for:
#    double py_max_subset_sparse(double* x, int n, int S, int cardS, struct fm_env_sparse* env)
# pyw.max_subset_sparse(x, n, S, cardS, env)


# Test wrapper for:
#    double py_ChoquetMob_sparse(double* x, int n, struct fm_env_sparse* env)
# pyw.ChoquetMob_sparse(x, n, env)


# Test wrapper for:
#    void py_ShapleyMob_sparse(double* v, int n, struct fm_env_sparse* out_env)
# pyw.ShapleyMob_sparse(v, n, out_env)


# Test wrapper for:
#    void py_BanzhafMob_sparse(double* v, int n, struct fm_env_sparse* out_env)
# pyw.BanzhafMob_sparse(v, n, out_env)


# Test wrapper for:
#    void py_populate_fm_2add_sparse(double* singletons, int numpairs, double* pairs, int* indicesp1, int* indicesp2, struct fm_env_sparse* out_env)
# pyw.populate_fm_2add_sparse(singletons, numpairs, pairs, indicesp1, indicesp2, out_env)


# Test wrapper for:
#    void py_add_pair_sparse(int i, int j, double v, struct fm_env_sparse* out_env)
# pyw.add_pair_sparse(i, j, v, out_env)


# Test wrapper for:
#    void py_add_tuple_sparse(int tupsize, int* tuple, double v, struct fm_env_sparse* out_env)
# pyw.add_tuple_sparse(tupsize, tuple, v, out_env)


# Test wrapper for:
#    void py_populate_fm_2add_sparse_from2add(int n, double* v, struct fm_env_sparse* out_env)
# pyw.populate_fm_2add_sparse_from2add(n, v, out_env)


# Test wrapper for:
#    void py_expand_2add_full(double* v, struct fm_env_sparse* out_env)
# pyw.expand_2add_full(v, out_env)


# Test wrapper for:
#    void py_expand_sparse_full(double* v, struct fm_env_sparse* out_env)
# pyw.expand_sparse_full(v, out_env)


# Test wrapper for:
#    void py_sparse_get_singletons(int n, double* v, struct fm_env_sparse* out_env)
# pyw.sparse_get_singletons(n, v, out_env)


# Test wrapper for:
#    int py_sparse_get_pairs(int* pairs, double* v, struct fm_env_sparse* env)
# pyw.sparse_get_pairs(pairs, v, env)


# Test wrapper for:
#    int py_sparse_get_tuples(int* tuples, double* v, struct fm_env_sparse* env)
# pyw.sparse_get_tuples(tuples, v, env)


# Test wrapper for:
#    int   py_generate_fm_2additive_convex_sparse(int n, struct fm_env_sparse* env)
# pyw.generate_fm_2additive_convex_sparse(n, env)


# Test wrapper for:
#    int   py_generate_fm_kadditive_convex_sparse(int n, int k, int nonzero, struct fm_env_sparse* env)
# pyw.generate_fm_kadditive_convex_sparse(n, k, nonzero, env)


# Test wrapper for:
#    void py_Nonmodularityindex_sparse(double* w, int n, struct fm_env_sparse* out_env)
# pyw.Nonmodularityindex_sparse(w, n, out_env)


pyw.fm_free( env);

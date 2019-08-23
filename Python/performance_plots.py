from consistency_checks import *


VD = [0.1, 0.2, 0.3, 0.4]  # viewing duration in sec


def plot_meta_data(plot_file):
    # todo: fix wrong trial count for second Quest block of subj1 day1
    y_values = OrderedDict(
        {
            'Quest': 0,
            'Block2': 1,
            'Block3': 2,
            'Block4': 3,
            'Block5': 4,
            'Block6': 5,
            'Block7': 6,
            'Block8': 7,
            'Block9': 8,
            'Block10': 9,
            'Block11': 10
        }
    )

    lines = []
    for p, c in PCP_COLORS.items():
        lines.append(mlines.Line2D([], [],
                                   linewidth=LINEWIDTH, color=c,
                                   marker='+', markersize=MARKERSIZE,
                                   label=f'prob CP = {p}' if not isinstance(p, str) else p))
    delta_y = 3
    ddy = 1
    for i, value in enumerate(y_values.keys()):
        y_values[value] = i * delta_y

    """first we process the metadata"""
    max_num_days, metadata, block_counts = super_power_metadata()

    """actual plotting"""

    # create figure
    fig, axes = plt.subplots(NUM_SUBJECTS, max_num_days + 1, figsize=(20, 26), sharey='col', sharex=False)
    all_dates = {}
    all_titles = {}
    dy_dict = {}
    for i in range(NUM_SUBJECTS):
        for j in range(max_num_days):
            all_dates[(i, j)] = []
            all_titles[(i, j)] = 0
            dy_dict[(i, j)] = -1
    # loop through subjects
    scount = -1
    for k, v in metadata.items():
        scount += 1
        # print(list(zip(
        #     list(v.keys()),
        #     [dc['day_count'] for dc in v.values()]
        # )))
        # loop through sessions
        for kk, vv in v.items():
            list_of_blocks = metadata[k][kk]['blocks']
            num_blocks = len(list_of_blocks)
            day_count = vv['day_count']
            all_titles[(scount, day_count)] = vv['rel_day']
            try:
                curr_ax = axes[scount, day_count]
            except IndexError:
                print(scount, day_count)
                raise

            # loop over blocks
            for block in list_of_blocks:

                if block['name'] == 'Quest':
                    linecolor = PCP_COLORS[block['name']]
                else:
                    linecolor = PCP_COLORS[PROB_CP[block['name']]]

                if not block['in_meta_not_in_file']:
                    list_of_datetimes = [block['datetime_start'], block['datetime_stop']]
                    all_dates[(scount, day_count)] += list_of_datetimes
                    dy_dict[(scount, day_count)] += delta_y
                    dy = y_values[block['name']]
                    dates = matplotlib.dates.date2num(list_of_datetimes)
                    # next two lines for debugging
                    # if (scount, day_count) == (0, 0):
                    #     print(kk, block['name'], dates)
                    curr_ax.plot_date(dates, [dy, dy],
                                      fmt='-+', linewidth=LINEWIDTH, markersize=MARKERSIZE,
                                      color=linecolor, xdate=True)
                    # annotate block number
                    bname = block['name']
                    if bname not in {'Quest', 'Block2'}:
                        bnum = re.findall('\\d+', bname)[0]
                        # bnum = bname[-1]
                        curr_ax.annotate(bnum + ':' + str(block['num_trials']), (dates[0], dy+.5), fontsize=SMALL_FONT)
                    else:
                        curr_ax.annotate(str(block['num_trials']), (dates[0], dy+.5), fontsize=SMALL_FONT)
    # print()
    # pprint.pprint(all_dates[(0, 0)])
    # pprint.pprint(matplotlib.dates.date2num(all_dates[(0, 0)]))
    # print()
    DX = .13
    for subj in range(NUM_SUBJECTS):
        for dd in range(max_num_days):
            if (subj, dd) in {(3, 2), (4, 2)}:
                continue
            curr_ax = axes[subj, dd]

            curr_ax.set_title('day ' + str(all_titles[(subj, dd)]))
            if dd == 0:
                curr_ax.set_ylabel('subj ' + str(subj + 1))
            curr_ax.tick_params(
                axis='y',  # changes apply to the x-axis
                which='both',  # both major and minor ticks are affected
                left=False,  # ticks along the bottom edge are off
                right=False,  # ticks along the top edge are off
                labelleft=False)  # labels along the bottom edge are off
            curr_ax.spines['top'].set_visible(False)
            curr_ax.spines['right'].set_visible(False)
            curr_ax.spines['bottom'].set_visible(False)
            curr_ax.spines['left'].set_visible(False)
            # orig_y1, orig_y2 = curr_ax.get_ylim()
            curr_ax.set_ylim(min(y_values.values())-3*ddy, max(y_values.values())+3*ddy)
            curr_ax.set_ylim(min(y_values.values())-3*ddy, max(y_values.values())+3*ddy)
            orig_x1, orig_x2 = curr_ax.get_xlim()
            curr_ax.set_xlim(orig_x1, orig_x1 + DX)

            try:
                xticks = [matplotlib.dates.num2date(x) for x in curr_ax.get_xticks()]
                curr_ax.set_xticklabels([d.strftime('%H:%M') for d in xticks], fontsize=SMALL_FONT)
            except ValueError:
                print('')
                print('Could not set xticks for subject', subj, 'day', dd)
                # print(curr_ax.get_xticks())

            # curr_ax.format_xdata = matplotlib.dates.DateFormatter('%H:%M')
            curr_ax.grid(b=True)
    fig.delaxes(axes[3, 2])
    fig.delaxes(axes[4, 2])
    plt.legend(handles=lines, bbox_to_anchor=(-1.1, 1.3), loc=2, borderaxespad=0., fontsize=2*SMALL_FONT)
    plt.subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=None, hspace=.7)

    def get_block_color(blockname):
        if blockname == 'Quest':
            return PCP_COLORS[blockname]
        else:
            pcp = PROB_CP[blockname]
            return PCP_COLORS[pcp]

    # plot block counts in right-most column
    for subj in range(NUM_SUBJECTS):
        curr_ax = axes[subj, max_num_days]
        counts_dict = block_counts[subj]

        # dict with key-val = <block name>:<index on x axis>
        xindices = {k:x for x, k in enumerate(y_values.keys())}
        # print(xindices)
        xs, ys, cs = [], [], []  # x values, y values and color values
        for k, v in counts_dict.items():
            xs.append(xindices[k])
            ys.append(v)
            cs.append(get_block_color(k))
        curr_ax.barh(xs, ys, color=cs)
        curr_ax.set_yticks(list(xindices.values()))
        yticklabels = ['Q'] + [str(i) for i in range(2,12)]
        curr_ax.set_yticklabels(yticklabels)
        curr_ax.set_xlabel('block count', fontsize=1.8*SMALL_FONT)
        curr_ax.set_xlim(0, 4)
        for label in (curr_ax.get_xticklabels() + curr_ax.get_yticklabels()):
            label.set_fontsize(SMALL_FONT)
    plt.savefig(plot_file)
    # plt.show()


def pcorrect_coh_all_subj_plot():
    """
    Produce plot https://scienceprojects.altervista.org/plots/coh_perf_block2.html (as of 08/20/2019)
    :return:
    """
    max_num_days, metadata, block_counts = super_power_metadata()
    fig, axes = plt.subplots(NUM_SUBJECTS, max_num_days + 1, figsize=(25, 21), sharey=True, sharex=False)
    plt.subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=.1, hspace=.2)

    def get_first_session_of_day(dict_of_sessions, day_count):
        for sess, content in dict_of_sessions.items():
            if content['day_count'] < day_count:
                continue
            else:
                return sess

    for subj in range(NUM_SUBJECTS):
        # # debug
        # if subj < NUM_SUBJECTS-1:
        #     continue
        subj_name = SUBJECT_NAMES[subj]
        bottom_label = True  # use the following to only draw xlabel on bottom-most panels: subj == NUM_SUBJECTS - 1
        for day in range(max_num_days):
            if (subj, day) in {(3, 2), (4, 2)}:
                continue
            curr_ax = axes[subj, day]
            subj_info = metadata[subj_name]
            first_session = get_first_session_of_day(subj_info, day)
            left_label = day == 0

            pcorrect_coh_plot(subj_name, first_session, curr_ax, figure=fig,
                              bottom_left_labels=(bottom_label, left_label))
            if day == 0:
                curr_ax.set_ylabel('subj ' + str(subj + 1))
            if subj < NUM_SUBJECTS - 1:
                curr_ax.tick_params(axis='x', labelsize=SMALL_FONT)
            elif subj == NUM_SUBJECTS - 1:
                curr_ax.set_xlabel('coherence', fontsize=MEDIUM_FONT)

    fig.delaxes(axes[3, 2])
    fig.delaxes(axes[4, 2])

    # plot all Block2 data together in right-most column
    for subj in range(NUM_SUBJECTS):
        ax = axes[subj, max_num_days]
        all_block2, _ = get_block_data('Block2', subject_name=SUBJECT_NAMES[subj])
        all_block2 = all_block2[all_block2['viewingDuration'] == .4]
        y_vals, y_err, trial_numbers = build_y_axis_pcorrect(all_block2,
                                                             err_margin=(.01, .99), err_method='Bayes')
        x_vals = all_block2['coherence'].unique()
        x_vals.sort()

        # plot the points
        ax.errorbar(x_vals, y_vals, yerr=y_err, fmt='o')
        for xcoh, tn in enumerate(trial_numbers):
            ax.annotate(str(tn), (x_vals[xcoh] + 2, y_vals[xcoh]), fontsize=SMALL_FONT)

        if subj == 0:
            ax.set_title("All block 2's", fontsize=MEDIUM_FONT)

        ax.tick_params(axis='y', labelright=True, right=True, labelsize=MEDIUM_FONT)
        ax.set_ylabel('P(Correct)', fontsize=MEDIUM_FONT, rotation=90)
        ax.yaxis.set_label_position("right")

        ax.set_xticks(x_vals)
        ax.set_xlim(-2, 103)
        ax.tick_params(axis='x', labelsize=SMALL_FONT)

        # ax.set_ylim(0, 1.2)
    # plt.show()
    for ax in axes.flat:
        ax.axhline(.5, linestyle='--', color='k')
        ax.axhline(1, linestyle='--', color='k')
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
    plt.savefig('coh_perf_Block2.png')


def pcorrect_vd_all_subj_probcp_plot(by_presence_cp=True, by_coh=True):
    """
    Plot percent correct as function of viewing duration, by subject, by probCP, by presenceCP
    :return:
    """
    if by_coh and not by_presence_cp:
        raise NotImplementedError

    # unique prob_cp values
    prob_cp_vals = np.unique(list(PROB_CP.values()))
    num_cp_vals = len(prob_cp_vals)

    if by_presence_cp:
        num_cols = 2 * num_cp_vals - 1  # number of columns in grid plot
        pcp_idxs = []  # list of length num_cols containing indices for prob_cp_vals
        for ii in range(num_cp_vals):
            if ii == 0:
                assert prob_cp_vals[ii] == 0, 'ordered sequence of prob_cp values does not contain 0 as first entry'
                pcp_idxs.append(ii)
            else:  # cols with Prob CP >0 take up two columns
                pcp_idxs.append(ii)
                pcp_idxs.append(ii)
        fwidth = 40
    else:
        num_cols = num_cp_vals
        pcp_idxs = list(range(num_cp_vals))
        fwidth = 25

    # create figure and axes
    fig, axes = plt.subplots(NUM_SUBJECTS, num_cols, figsize=(fwidth, 21), sharey=False, sharex=False)
    plt.subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=.2, hspace=.2)
    axes_to_skip = {(0,5), (0,6)}
    fig.delaxes(axes[0, 5])
    fig.delaxes(axes[0, 6])
    # loop over subjects
    for subj in range(NUM_SUBJECTS):
        subj_name = SUBJECT_NAMES[subj]
        if by_presence_cp:
            with_cp = 0  # switch that decides whether to filter trials with a CP (1) or not (0)
            colors = {0: 'blue', 1: 'red'}  # plots for no-CP trials in blue, plots for CP-trials in red
        for col in range(num_cols):
            pcp_idx = pcp_idxs[col]
            prob_cp = prob_cp_vals[pcp_idx]
            if (subj, col) in axes_to_skip:
                continue
            ax = axes[subj, col]
            all_probcp = get_probcp_data(prob_cp, subject_name=subj_name)

            if by_presence_cp:
                all_probcp = all_probcp[all_probcp['presenceCP'] == with_cp]

            if len(all_probcp) == 0:
                continue

            if by_coh:
                # split coherence in three categories, zero (z), threshold (th) and 1 hundred (h)
                zcoh_df = all_probcp[all_probcp['coherence'] == 0]
                if len(zcoh_df) > 0:
                    y_vals_z, y_err_z, trial_num_z = build_y_axis_pcorrect_xvd(
                        zcoh_df, err_margin=(.01, .99), err_method='Bayes'
                    )
                else:
                    y_vals_z, y_err_z, trial_num_z = None, None, None

                thcoh_df = all_probcp[(all_probcp['coherence'] > 0) & (all_probcp['coherence'] < 100)]
                if len(thcoh_df) > 0:
                    y_vals_th, y_err_th, trial_num_th = build_y_axis_pcorrect_xvd(
                        thcoh_df, err_margin=(.01, .99), err_method='Bayes'
                    )
                else:
                    y_vals_th, y_err_th, trial_num_th = None, None, None

                hcoh_df = all_probcp[all_probcp['coherence'] == 100]
                if len(hcoh_df) > 0:
                    y_vals_h, y_err_h, trial_num_h = build_y_axis_pcorrect_xvd(
                        hcoh_df, err_margin=(.01, .99), err_method='Bayes'
                    )
                else:
                    y_vals_h, y_err_h, trial_num_h = None, None, None
            else:
                y_vals, y_err, trial_numbers = build_y_axis_pcorrect_xvd(all_probcp, err_margin=(.01, .99),
                                                                         err_method='Bayes')
            x_vals = all_probcp['viewingDuration'].unique()
            x_vals.sort()

            # plot the points
            if by_presence_cp:
                if by_coh:
                    z_jitter = -.01
                    h_jitter = .01
                    legend = []
                    if y_vals_z is not None:
                        ax.errorbar(x_vals + z_jitter, y_vals_z, yerr=y_err_z, fmt='o', color=colors[with_cp],
                                    fillstyle='none', markersize=MARKERSIZE*.8)
                        legend.append('0-coh')

                    if y_vals_th is not None:
                        ax.errorbar(x_vals, y_vals_th, yerr=y_err_th, fmt='*', color=colors[with_cp],
                                    markersize=MARKERSIZE*.8)
                        legend.append('th-coh')

                    if y_vals_h is not None:
                        ax.errorbar(x_vals + h_jitter, y_vals_h, yerr=y_err_h, fmt='^', fillstyle='none',
                                    color=colors[with_cp], markersize=MARKERSIZE*.8)
                        legend.append('100-coh')

                    # legend
                    if col == 4 and subj_name == 'S1':
                        ax.legend(legend, bbox_to_anchor=(1, 1), loc=2, borderaxespad=0., fontsize=MEDIUM_FONT)

                else:
                    ax.errorbar(x_vals, y_vals, yerr=y_err, fmt='o', color=colors[with_cp])
                with_cp = 1 - with_cp  # flip for next column
            else:
                ax.errorbar(x_vals, y_vals, yerr=y_err, fmt='o', color=PCP_COLORS[prob_cp])

            if by_coh:
                for xidx, tn in enumerate(trial_num_z):
                    ax.annotate(str(tn), (x_vals[xidx] + .013, y_vals_z[xidx]), fontsize=SMALL_FONT)
                for xidx, tn in enumerate(trial_num_th):
                    ax.annotate(str(tn), (x_vals[xidx] + .013, y_vals_th[xidx]), fontsize=SMALL_FONT)
                for xidx, tn in enumerate(trial_num_h):
                    ax.annotate(str(tn), (x_vals[xidx] + .013, y_vals_h[xidx]), fontsize=SMALL_FONT)
            else:
                for xidx, tn in enumerate(trial_numbers):
                    ax.annotate(str(tn), (x_vals[xidx] + .013, y_vals[xidx]), fontsize=SMALL_FONT)

            if subj == 0:
                ax.set_title(f"Prob CP = {prob_cp}", fontsize=MEDIUM_FONT)
            elif subj == NUM_SUBJECTS - 1:
                ax.set_xlabel('duration')

            if prob_cp == 0:
                ax.set_ylabel(subj_name, fontsize=MEDIUM_FONT)
            elif prob_cp == max(prob_cp_vals):
                ax.yaxis.set_label_position("right")
                ax.set_ylabel('P(Correct)', fontsize=MEDIUM_FONT)

            ax.set_xticks(x_vals)
            ticks = np.arange(0.1, 1.1, 0.2)
            # labels = [f"{x:.1f}" for x in ticks]
            ax.set_yticks(ticks)  # todo: still not happy with yticks in this plot

            ax.set_xlim(0, .5)
            ax.set_ylim(.2, 1.1)

            ax.tick_params(axis='both', labelleft=True, left=True, labelbottom=True, bottom=True, labelsize=SMALL_FONT)

        # ax.set_ylim(0, 1.2)
    # plt.show()
    for ax in axes.flat:
        ax.axhline(.5, linestyle='--', color='k')
        ax.axhline(1, linestyle='--', color='k')
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)

    if by_presence_cp:
        title = 'No-CP trials in BLUE, CP-trials in RED'
        fig.suptitle(title, fontsize=LARGE_FONT)
        if by_coh:
            file_to_save = IMAGE_SAVE_FOLDER + 'vd_perf_all_prob_cp_by_coh' + '.png'
        else:
            file_to_save = IMAGE_SAVE_FOLDER + 'vd_perf_all_prob_cp' + '.png'
    else:
        file_to_save = IMAGE_SAVE_FOLDER + 'vd_perf_all_prob_cp' + '_.png'
    plt.savefig(file_to_save)
    # plt.show()


def pcorrect_coh_all_subj_probcp_plot(vd_filter=0.4):
    """
    Plot percent correct as function of coherence, by subject, by probCP, by presenceCP
    :param vd_filter: (float) the viewing duration through which data should be filtered. Default 400 msec.
    :return:
    """
    # get superpower metadata
    # max_num_days, metadata, block_counts = super_power_metadata()

    # unique prob_cp values
    prob_cp_vals = np.unique(list(PROB_CP.values()))
    prob_cp_vals.sort()

    num_cp_vals = len(prob_cp_vals)

    num_cols = 2 * num_cp_vals - 1  # number of columns in grid plot

    pcp_idxs = []  # list of length num_cols containing indices for prob_cp_vals
    for ii in range(num_cp_vals):
        if ii == 0:
            assert prob_cp_vals[ii] == 0, 'ordered sequence of prob_cp values does not contain 0 as first entry'
            pcp_idxs.append(ii)
        else:  # cols with Prob CP >0 take up two columns
            pcp_idxs.append(ii)
            pcp_idxs.append(ii)

    # create figure and axes
    fig, axes = plt.subplots(NUM_SUBJECTS, num_cols, figsize=(40, 21), sharey=False, sharex=False)
    plt.subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=.2, hspace=.2)

    # loop over subjects
    for subj in range(NUM_SUBJECTS):
        subj_name = SUBJECT_NAMES[subj]
        with_cp = 0  # switch that decides whether to filter trials with a CP (1) or not (0)
        colors = {0: 'blue', 1: 'red'}  # plots for no-CP trials in blue, plots for CP-trials in red
        for col in range(num_cols):
            pcp_idx = pcp_idxs[col]
            prob_cp = prob_cp_vals[pcp_idx]
            ax = axes[subj, col]
            all_probcp = get_probcp_data(prob_cp, subject_name=subj_name)
            all_probcp = all_probcp[(all_probcp['viewingDuration'] == vd_filter) &
                                    (all_probcp['presenceCP'] == with_cp)]

            y_vals, y_err, trial_numbers = build_y_axis_pcorrect(all_probcp,
                                                                 err_margin=(.01, .99), err_method='Bayes')
            x_vals = all_probcp['coherence'].unique()
            x_vals.sort()

            # plot the points
            ax.errorbar(x_vals, y_vals, yerr=y_err, fmt='o', color=colors[with_cp])

            with_cp = 1 - with_cp  # flip for next column

            for xcoh, tn in enumerate(trial_numbers):
                ax.annotate(str(tn), (x_vals[xcoh] + 2, y_vals[xcoh]), fontsize=SMALL_FONT)

            if subj == 0:
                ax.set_title(f"Prob CP = {prob_cp}", fontsize=MEDIUM_FONT)
            elif subj == NUM_SUBJECTS - 1:
                ax.set_xlabel('coherence')

            if prob_cp == 0:
                ax.set_ylabel(subj_name, fontsize=MEDIUM_FONT)
            elif prob_cp == max(prob_cp_vals):
                ax.yaxis.set_label_position("right")
                ax.set_ylabel('P(Correct)', fontsize=MEDIUM_FONT)

            ax.set_xticks(x_vals)
            ticks = np.arange(0.2, 1.1, 0.2)
            # labels = [f"{x:.1f}" for x in ticks]
            ax.set_yticks(ticks)  # todo: still not happy with yticks in this plot

            ax.set_xlim(-2, 103)
            ax.set_ylim(.2, 1.1)

            ax.tick_params(axis='both', labelleft=True, left=True, labelbottom=True, bottom=True, labelsize=SMALL_FONT)

        # ax.set_ylim(0, 1.2)
    # plt.show()
    for ax in axes.flat:
        ax.axhline(.5, linestyle='--', color='k')
        ax.axhline(1, linestyle='--', color='k')
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)

    vd_msec = str(int(1000*vd_filter))
    title = 'Viewing Duration = ' + vd_msec + ' msec; No-CP trials in BLUE, CP-trials in RED'
    fig.suptitle(title, fontsize=LARGE_FONT)

    file_to_save = IMAGE_SAVE_FOLDER + 'coh_perf_all_prob_cp_' + vd_msec + '.png'
    plt.savefig(file_to_save)
    # plt.show()


def build_y_axis_pcorrect(data, err_margin=(.01, .99), err_method='Bayes'):
    """
    computes percent correct with error bars as a function of coherence in the given dataframe
    :param data: pandas.DataFrame with valid data
    :param err_margin: percentiles that define CI or region of posterior
    :param err_method: either 'Bayes' or 'CI'
    :return:
    """
    percent_correct, errors, coh_trial_counts = [], [], []

    def get_coh_values(dataframe):
        assert dataframe['coherence'].isna().sum() == 0, 'some nan values in coherence column'
        coh_vals = dataframe['coherence'].unique()
        coh_vals.sort()
        return coh_vals

    for coh_val in get_coh_values(data):
        extracted_df = data[data['coherence'] == coh_val].copy()
        num_nan = extracted_df['dirCorrect'].isna().sum()

        data_point = extracted_df['dirCorrect'].mean()
        percent_correct.append(data_point)

        # compute error bars
        num_trials = len(extracted_df) - num_nan
        coh_trial_counts.append(num_trials)
        num_correct = extracted_df['dirCorrect'].sum()
        num_incorrect = num_trials - num_correct

        if err_method == 'Bayes':
            # compute Beta posterior
            if coh_val == 0:
                alpha_prior, beta_prior = 3.6, 3.6
            elif coh_val == 100:
                alpha_prior, beta_prior = 3, 1
            else:
                alpha_prior, beta_prior = 2.85, 2.33
            b_alpha = alpha_prior + num_correct
            b_beta = beta_prior + num_incorrect

            # find quantiles of the posterior
            percentiles = sst.beta.ppf(err_margin, b_alpha, b_beta)
            errors.append([abs(xx - data_point) for xx in percentiles])
        else:
            pihat = num_correct / num_trials
            stderr = np.sqrt(pihat * (1-pihat) / num_trials)
            low_err = -sst.norm.ppf(err_margin[0]) * stderr
            high_err = sst.norm.ppf(err_margin[1]) * stderr
            errors.append([low_err, high_err])
    return percent_correct, np.transpose(np.array(errors)), coh_trial_counts


def build_y_axis_pcorrect_xvd(data, err_margin=(.01, .99), err_method='Bayes'):
    """
    computes percent correct with error bars as a function of VD in the given dataframe
    :param data: pandas.DataFrame with valid data
    :param err_margin: percentiles that define CI or region of posterior
    :param err_method: either 'Bayes' or 'CI'
    :return:
    """
    percent_correct, errors, vd_trial_counts = [], [], []

    def get_vd_values(dataframe):
        assert dataframe['viewingDuration'].isna().sum() == 0, 'some nan values in viewing duration column'
        vd_vals = dataframe['viewingDuration'].unique()
        vd_vals.sort()
        assert set(vd_vals).issubset(set(VD)), f'vd_vals: {vd_vals}; VD: {VD}; {data.head()}'
        return vd_vals

    for vd_val in get_vd_values(data):
        extracted_df = data[data['viewingDuration'] == vd_val].copy()
        num_nan = extracted_df['dirCorrect'].isna().sum()

        data_point = extracted_df['dirCorrect'].mean()
        percent_correct.append(data_point)

        # compute error bars
        num_trials = len(extracted_df) - num_nan
        vd_trial_counts.append(num_trials)
        num_correct = extracted_df['dirCorrect'].sum()
        num_incorrect = num_trials - num_correct

        if err_method == 'Bayes':
            # compute Beta posterior
            alpha_prior, beta_prior = 1, 1
            b_alpha = alpha_prior + num_correct
            b_beta = beta_prior + num_incorrect

            # find quantiles of the posterior
            percentiles = sst.beta.ppf(err_margin, b_alpha, b_beta)
            errors.append([abs(xx - data_point) for xx in percentiles])
        else:
            pihat = num_correct / num_trials
            stderr = np.sqrt(pihat * (1-pihat) / num_trials)
            low_err = -sst.norm.ppf(err_margin[0]) * stderr
            high_err = sst.norm.ppf(err_margin[1]) * stderr
            errors.append([low_err, high_err])
    return percent_correct, np.transpose(np.array(errors)), vd_trial_counts


def pcorrect_coh_plot(subject, session_timestamp, ax, err_method='Bayes', detail=True, figure=None,
                      bottom_left_labels=(True, True)):
    """
    plots the following in the given axis, with data from 400-msec trials of Block2:
        percent correct as function of coherence, with error bars
        inset with coherence as function of trialIndex in Quest block
    """
    assert err_method in {'Bayes', 'CI'}, 'error method unknown'
    if detail:
        assert figure is not None

    # get the metadata from the Quest block
    meta_data = read_new_metadata()
    blocks = meta_data[subject][session_timestamp]['blocks']

    def extract_quest_parameters():
        for b in blocks:
            if b['name'] == 'Quest':
                params = tuple(b['quest'])
                threshold, slope, guess_rate, lapse_rate = params
                return threshold, slope, guess_rate, lapse_rate

    def extract_block2_dataframe():
        whole_block, _ = get_block_data('Block2', stamp=session_timestamp)
        block_to_return = whole_block[whole_block['viewingDuration'] == .4]
        # pprint.pprint(block_to_return.head())
        return block_to_return

    def build_x_axis():
        th, _, __, ___ = extract_quest_parameters()
        if th == 100:
            return 0, 100
        else:
            return 0, th, 100

    def weibull(x, guess, lapse, alpha, beta):
        p_success = guess + (1 - guess - lapse) * (1 - np.exp(-(x / alpha)**beta))
        return p_success  # 1-np.exp(-((x/alpha)**beta))

    x_vals = build_x_axis()
    y_vals, y_err, trial_numbers = build_y_axis_pcorrect(extract_block2_dataframe(),
                                                         err_margin=(.01, .99), err_method=err_method)

    # plot the points with error bars
    try:
        ax.errorbar(x_vals, y_vals, yerr=y_err, fmt='o')
    except ValueError:
        print(subject, session_timestamp, x_vals, y_vals)
        raise

    # plot the Weibull
    x_weibull = np.linspace(0, 100)
    qthreshold, qslope, qguess_rate, qlapse_rate = extract_quest_parameters()
    y_weibull = weibull(x_weibull, qguess_rate, qlapse_rate, qthreshold, qslope)

    ax.plot(x_weibull, y_weibull)

    for xcoh, tn in enumerate(trial_numbers):
        ax.annotate(str(tn), (x_vals[xcoh]+2, y_vals[xcoh]), fontsize=SMALL_FONT)

    ax.set_title(session_timestamp, fontsize=MEDIUM_FONT)
    ax.tick_params(
        axis='both',
        labelbottom=bottom_left_labels[0],
        labelleft=bottom_left_labels[1],
        labelsize=MEDIUM_FONT
    )
    # if bottom_left_labels[1]:
    #     ax.set_ylabel('P(Correct)', fontsize=MEDIUM_FONT)
    # if bottom_left_labels[0]:
    #     ax.set_xlabel('coherence', fontsize=MEDIUM_FONT)
    ax.set_xlim(-2, 103)
    ax.set_ylim(0.25, 1.1)

    # plot inset optionally
    if detail:
        # These are in unitless percentages of the figure size. (0,0 is bottom left)
        container_pos = ax.get_position()
        delta_h, delta_w = 0.01 * container_pos.height, 0.01 * container_pos.width
        # print(container_pos)
        left = container_pos.x0 + .5 * container_pos.width
        bottom = container_pos.y0 + delta_h
        width = container_pos.x1 - left - delta_w
        height = .5 * container_pos.height
        ax2 = figure.add_axes([left, bottom, width, height])
        quest_data, _ = get_block_data('Quest', stamp=session_timestamp)
        quest_data = quest_data[quest_data['dirChoice'].notnull()]
        ax2.step(quest_data['trialIndex'], quest_data['coherence'])
        ax2.tick_params(
            axis='x',  # changes apply to the x-axis
            which='both',  # both major and minor ticks are affected
            bottom=False,  # ticks along the bottom edge are off
            top=False,  # ticks along the top edge are off
            labelbottom=False)  # labels along the bottom edge are off
        for tick in ax2.yaxis.get_major_ticks():
            tick.label.set_fontsize(SMALL_FONT)


if __name__ == '__main__':
    # read_new_metadata()  # a quick way to do a check sum on metadata
    # plot_meta_data('metadata.png')
    # pcorrect_coh_all_subj_plot()  # Quest + Block2
    # for vd in [.1, .2, .3, .4]:
    #     pcorrect_coh_all_subj_probcp_plot(vd_filter=vd)  # Perf by subject by PROB_CP
    # pcorrect_vd_all_subj_probcp_plot(by_presence_cp=True)
    pcorrect_vd_all_subj_probcp_plot(by_presence_cp=True, by_coh=True)
